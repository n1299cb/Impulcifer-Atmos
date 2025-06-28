# This file is part of Earprint, a modified version of Impulcifer.
# Original code © 2018 Jaakko Pasanen — licensed under the MIT License.
# Modifications © 2025 Blaring Sound LLC — also licensed under the MIT License unless otherwise stated.
"""Real-time convolution engine for binaural rendering."""

from __future__ import annotations

import numpy as np
from typing import Dict, Optional, Tuple, Union

try:
    import sounddevice as sd
except Exception:  # pragma: no cover - optional dependency may be missing
    sd = None
from utils import read_wav
import threading
from impulse_response import ImpulseResponse
from hrir import HRIR
from constants import HEXADECAGONAL_TRACK_ORDER


class RealTimeConvolver:
    """Low-latency convolution engine for binaural rendering."""

    def __init__(
        self,
        irs: Union[HRIR, Dict[float, Tuple[np.ndarray, np.ndarray]]],
        samplerate: Optional[int] = None,
        block_size: int = 1024,
    ) -> None:
        self.block_size = block_size
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._yaw = 0.0

        if isinstance(irs, dict):
            if samplerate is None:
                raise ValueError("samplerate must be given for BRIR dictionaries")
            self.fs = samplerate
            self.brirs: Dict[float, Tuple[np.ndarray, np.ndarray]] = {
                float(a): (np.asarray(l), np.asarray(r)) for a, (l, r) in irs.items()
            }
            self.angles = sorted(self.brirs.keys())
            self._prepare_ir_fft_brirs()
            self.n_speakers = 2
        else:
            self.fs = irs.fs
            self.speakers = list(irs.irs.keys())
            self.n_speakers = len(self.speakers)
            self._prepare_ir_fft_hrir(irs)

        self.overlap = np.zeros((2, self.fft_size - self.block_size))

    def _next_pow2(self, x: int) -> int:
        return 1 << (x - 1).bit_length()

    def _prepare_ir_fft_hrir(self, hrir) -> None:
        max_len = 0
        for pair in hrir.irs.values():
            max_len = max(max_len, len(pair["left"].data), len(pair["right"].data))
        self.fft_size = self._next_pow2(self.block_size + max_len - 1)
        self.ir_fft = {}
        for name, pair in hrir.irs.items():
            self.ir_fft[name] = {}
            for ear in ("left", "right"):
                buf = np.zeros(self.fft_size)
                data = pair[ear].data
                buf[: len(data)] = data
                self.ir_fft[name][ear] = np.fft.rfft(buf)

    def _prepare_ir_fft_brirs(self) -> None:
        max_len = 0
        for left, right in self.brirs.values():
            max_len = max(max_len, len(left), len(right))
        self.fft_size = self._next_pow2(self.block_size + max_len - 1)
        self.ir_fft = {}
        for angle, (left, right) in self.brirs.items():
            buf_l = np.zeros(self.fft_size)
            buf_l[: len(left)] = left
            buf_r = np.zeros(self.fft_size)
            buf_r[: len(right)] = right
            self.ir_fft[angle] = {
                "left": np.fft.rfft(buf_l),
                "right": np.fft.rfft(buf_r),
            }

    def process_block(self, block: np.ndarray) -> np.ndarray:
        """Process single audio block.

        Args:
            block: Array ``(n_speakers, block_size)``.

        Returns:
            Stereo output block ``(2, block_size)``.
        """
        if hasattr(self, "brirs"):
            if block.shape != (2, self.block_size):
                raise ValueError("Invalid input block shape")
            angle = min(self.angles, key=lambda a: abs(a - self._yaw))
            ir = self.ir_fft[angle]
            buf = np.zeros((2, self.fft_size))
            buf[:, : self.block_size] = block
            buf_fft = np.fft.rfft(buf, axis=1)
            out_l = buf_fft[0] * ir["left"]
            out_r = buf_fft[1] * ir["right"]
        else:
            if block.shape != (self.n_speakers, self.block_size):
                raise ValueError("Invalid input block shape")
            buf = np.zeros((self.n_speakers, self.fft_size))
            buf[:, : self.block_size] = block
            buf_fft = np.fft.rfft(buf, axis=1)
            out_l = np.zeros(self.fft_size // 2 + 1, dtype=complex)
            out_r = np.zeros_like(out_l)
            for i, name in enumerate(self.speakers):
                out_l += buf_fft[i] * self.ir_fft[name]["left"]
                out_r += buf_fft[i] * self.ir_fft[name]["right"]

        y_l = np.fft.irfft(out_l)
        y_r = np.fft.irfft(out_r)

        y_l[: self.overlap.shape[1]] += self.overlap[0]
        y_r[: self.overlap.shape[1]] += self.overlap[1]

        self.overlap[0] = y_l[self.block_size :]
        self.overlap[1] = y_r[self.block_size :]

        return np.stack([y_l[: self.block_size], y_r[: self.block_size]])

    def set_yaw(self, yaw: float) -> None:
        """Update current head orientation."""
        self._yaw = float(yaw)

    def start(
        self,
        duration: Optional[float] = None,
        input_device: Optional[Union[int, str]] = None,
        output_device: Optional[Union[int, str]] = None,
        latency: float | None = None,
    ) -> None:
        """Start real-time convolution in a background thread."""
        if self._thread is not None:
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self.run,
            kwargs={
                "duration": duration,
                "input_device": input_device,
                "output_device": output_device,
                "latency": latency,
            },
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """Stop the background convolution thread."""
        if self._thread is None:
            return
        self._stop.set()
        if sd:
            sd.stop()
        self._thread.join()
        self._thread = None

    def run(
        self,
        duration: Optional[float] = None,
        input_device: Optional[Union[int, str]] = None,
        output_device: Optional[Union[int, str]] = None,
        latency: float | None = None,
    ) -> None:
        """Run real-time convolution using ``sounddevice`` streams."""

        if sd is None:
            raise RuntimeError("sounddevice library not available")

        def callback(indata, outdata, frames, time_info, status):
            if status:
                print(status)
            block = np.transpose(indata)
            out_block = self.process_block(block)
            outdata[:] = np.transpose(out_block)

        with sd.Stream(
            samplerate=self.fs,
            blocksize=self.block_size,
            dtype="float32",
            channels=(self.n_speakers, 2),
            callback=callback,
            device=(input_device, output_device),
            latency=latency,
        ):
            if duration is None:
                while not self._stop.is_set():
                    sd.sleep(100)
            else:
                sd.sleep(int(duration * 1000))


def convolve_file(
    input_wav: str,
    output_wav: str,
    hrir,
    block_size: int = 1024,
) -> None:
    """Offline convolution helper for multi-channel files."""

    import soundfile as sf

    fs, hrir_fs = hrir.fs, hrir.fs
    data, fs_in = sf.read(input_wav, always_2d=True)
    if fs_in != fs:
        raise ValueError("Sampling rate mismatch")
    engine = RealTimeConvolver(hrir, block_size)
    out = []
    idx = 0
    data = np.transpose(data)
    while idx < data.shape[1]:
        block = data[:, idx : idx + block_size]
        if block.shape[1] < block_size:
            pad = np.zeros((data.shape[0], block_size - block.shape[1]))
            block = np.concatenate([block, pad], axis=1)
        out_block = engine.process_block(block)
        out.append(out_block)
        idx += block_size
    out = np.concatenate(out, axis=1)
    sf.write(output_wav, np.transpose(out), fs)


def _hrir_from_wav(file_path: str) -> HRIR:
    """Helper for loading ``hrir.wav`` into an ``HRIR`` object."""

    fs, data = read_wav(file_path, expand=True)
    estimator = type("_e", (), {"fs": fs})()
    h = HRIR(estimator)
    for ch_name, ch_data in zip(HEXADECAGONAL_TRACK_ORDER, data):
        speaker, side = ch_name.split("-")
        if speaker not in h.irs:
            h.irs[speaker] = {}
        h.irs[speaker][side] = ImpulseResponse(ch_data, fs)
    return h


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Offline BRIR convolution")
    parser.add_argument("input", help="Input multichannel WAV file")
    parser.add_argument("output", help="Output stereo WAV file")
    parser.add_argument("hrir", help="hrir.wav generated by Earprint")
    parser.add_argument("--block_size", type=int, default=1024)
    args = parser.parse_args()

    hrir_obj = _hrir_from_wav(args.hrir)
    convolve_file(args.input, args.output, hrir_obj, block_size=args.block_size)


# Backwards compatibility for earlier naming
RealtimeConvolver = RealTimeConvolver
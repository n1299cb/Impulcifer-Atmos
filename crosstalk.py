import numpy as np
from typing import Dict
from hrir import HRIR


def compute_crosstalk_filters(
    hrir: HRIR,
    left_speaker: str = "FL",
    right_speaker: str = "FR",
    length: int = 256,
    regularization: float = 1e-6,
) -> Dict[str, np.ndarray]:
    """Compute simple cross-talk cancellation FIR filters.

    Args:
        hrir: ``HRIR`` object containing speaker-ear impulse responses.
        left_speaker: Name of the speaker used for the left channel.
        right_speaker: Name of the speaker used for the right channel.
        length: Length of the output filters in samples.
        regularization: Diagonal loading factor to keep matrix inversion stable.

    Returns:
        Dictionary with keys ``"LL"``, ``"LR"``, ``"RL"`` and ``"RR"``.
    """
    h_ll = hrir.irs[left_speaker]["left"].data
    h_lr = hrir.irs[right_speaker]["left"].data
    h_rl = hrir.irs[left_speaker]["right"].data
    h_rr = hrir.irs[right_speaker]["right"].data

    max_len = max(len(h_ll), len(h_lr), len(h_rl), len(h_rr), length)
    fft_size = 1 << (max_len - 1).bit_length()

    def _rfft(data: np.ndarray) -> np.ndarray:
        buf = np.zeros(fft_size)
        buf[: len(data)] = data
        return np.fft.rfft(buf)

    H_ll = _rfft(h_ll)
    H_lr = _rfft(h_lr)
    H_rl = _rfft(h_rl)
    H_rr = _rfft(h_rr)

    F_ll = np.zeros_like(H_ll, dtype=complex)
    F_lr = np.zeros_like(H_ll, dtype=complex)
    F_rl = np.zeros_like(H_ll, dtype=complex)
    F_rr = np.zeros_like(H_ll, dtype=complex)

    eye = np.eye(2)
    for k in range(len(H_ll)):
        H = np.array([[H_ll[k], H_rl[k]], [H_lr[k], H_rr[k]]], dtype=complex)
        H += regularization * eye
        inv_H = np.linalg.inv(H)
        F_ll[k] = inv_H[0, 0]
        F_lr[k] = inv_H[0, 1]
        F_rl[k] = inv_H[1, 0]
        F_rr[k] = inv_H[1, 1]

    filters = {
        "LL": np.fft.irfft(F_ll, n=fft_size)[:length],
        "LR": np.fft.irfft(F_lr, n=fft_size)[:length],
        "RL": np.fft.irfft(F_rl, n=fft_size)[:length],
        "RR": np.fft.irfft(F_rr, n=fft_size)[:length],
    }
    return filters
from __future__ import annotations

import os
import time
from threading import Thread

import numpy as np

from models import PlaybackSettings
from realtime_convolution import RealTimeConvolver
from tracking import HeadTracker


class PlaybackViewModel:
    """ViewModel controlling real-time playback with head tracking."""

    def __init__(self) -> None:
        self.tracker: HeadTracker | None = None
        self.convolver: RealTimeConvolver | None = None
        self._thread: Thread | None = None
        self._running = False

    def _load_brirs(self, path: str) -> dict[float, tuple[list[float], list[float]]]:
        brirs: dict[float, tuple[list[float], list[float]]] = {}
        for file in os.listdir(path):
            if not file.endswith(".npz"):
                continue
            angle = float(os.path.splitext(file)[0])
            data = np.load(os.path.join(path, file))
            brirs[angle] = (data["left"], data["right"])
        return brirs

    def play(self, settings: PlaybackSettings) -> None:
        brirs = self._load_brirs(settings.brir_dir)
        self.tracker = HeadTracker(port=settings.osc_port)
        self.convolver = RealTimeConvolver(
            brirs,
            samplerate=settings.samplerate,
            block_size=settings.blocksize,
        )
        self.tracker.start()
        self.convolver.start()
        self._running = True

        def _loop() -> None:
            while self._running:
                if self.tracker:
                    self.convolver.set_yaw(self.tracker.yaw())
                time.sleep(0.01)

        self._thread = Thread(target=_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self.convolver:
            self.convolver.stop()
        if self.tracker:
            self.tracker.stop()
        if self._thread:
            self._thread.join()
            self._thread = None
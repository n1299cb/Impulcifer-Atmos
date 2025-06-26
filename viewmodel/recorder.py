from typing import List
import subprocess
import sys

from models import RecorderSettings


class RecordingViewModel:
    """ViewModel handling recording commands."""

    def run_recorder(self, settings: RecorderSettings) -> subprocess.CompletedProcess:
        args = [
            sys.executable,
            "recorder.py",
            "--output_channels",
            ",".join(str(c) for c in settings.output_channels),
            "--input_channels",
            ",".join(str(c) for c in settings.input_channels),
            "--playback_device",
            settings.playback_device,
            "--recording_device",
            settings.recording_device,
            "--output_dir",
            settings.measurement_dir,
            "--test_signal",
            settings.test_signal,
        ]
        if settings.output_file:
            args.extend(["--output_file", settings.output_file])
        return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def run_capture_wizard(
        self,
        layout_name: str,
        layout_groups: List[List[str]],
        settings: RecorderSettings,
        prompt_fn=None,
        message_fn=None,
    ) -> None:
        from capture_wizard import run_capture

        run_capture(
            layout_name,
            layout_groups,
            settings.measurement_dir,
            prompt_fn=prompt_fn,
            message_fn=message_fn,
            input_device=settings.recording_device,
            output_device=settings.playback_device,
        )

from typing import List
import subprocess
import sys
import os

from models import RecorderSettings


class RecordingViewModel:
    """ViewModel handling recording commands."""

    def run_recorder(self, settings: RecorderSettings, progress_callback=None) -> subprocess.CompletedProcess:
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
        if progress_callback is None:
            if settings.output_file:
                args.extend(["--output_file", settings.output_file])
            return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            from recorder import play_and_record

            record_path = settings.output_file or os.path.join(settings.measurement_dir, "recording.wav")
            play_and_record(
                play=settings.test_signal,
                record=record_path,
                input_device=settings.recording_device,
                output_device=settings.playback_device,
                channels=len(settings.output_channels) or 2,
                progress_callback=progress_callback,
            )
            return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")

    def run_capture_wizard(
        self,
        layout_name: str,
        layout_groups: List[List[str]],
        settings: RecorderSettings,
        prompt_fn=None,
        message_fn=None,
        progress_callback=None,
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
            progress_fn=progress_callback,
        )

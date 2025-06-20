import os
import argparse
from generate_layout import select_layout, init_layout
import recorder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STEREO_SWEEP = os.path.join(
    BASE_DIR,
    "data",
    "sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav",
)
DEFAULT_MONO_SWEEP = os.path.join(
    BASE_DIR,
    "data",
    "sweep-seg-FL-mono-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav",
)

def run_capture(
    layout_name: str,
    groups: list[list[str]],
    out_dir: str,
    stereo_sweep: str = DEFAULT_STEREO_SWEEP,
    mono_sweep: str = DEFAULT_MONO_SWEEP,
    prompt_fn=input,
    message_fn=print,
    **rec_kwargs,
) -> None:
    """Run interactive capture for each speaker group.

    ``prompt_fn`` is used to pause between recordings, while ``message_fn`` is
    used to display progress messages. Both default to the standard console
    implementations so the function can be reused in a GUI context by supplying
    custom callbacks.
    """

    message_fn(f"\nRecording layout '{layout_name}' into {out_dir}\n")
    os.makedirs(out_dir, exist_ok=True)

    prompt_fn(
        "Insert binaural microphones and wear headphones.\nPress Enter to record headphone response..."
    )
    recorder.play_and_record(
        play=stereo_sweep,
        record=os.path.join(out_dir, "headphones.wav"),
        channels=2,
        **rec_kwargs,
    )

    for group in groups:
        filename = ",".join(group) + ".wav"
        sweep = stereo_sweep if len(group) > 1 else mono_sweep
        channels = len(group)
        prompt = f"\nPosition for {filename} and press Enter to start recording..."
        prompt_fn(prompt)
        recorder.play_and_record(
            play=sweep,
            record=os.path.join(out_dir, filename),
            channels=channels,
            **rec_kwargs,
        )

    message_fn("\n✅ Capture completed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Step-by-step HRIR capture wizard")
    parser.add_argument("--layout", help="Layout name to use")
    parser.add_argument("--dir", default="data/test_capture", help="Target directory")
    parser.add_argument("--stereo_sweep", default=DEFAULT_STEREO_SWEEP,
                        help="Stereo sweep file")
    parser.add_argument("--mono_sweep", default=DEFAULT_MONO_SWEEP,
                        help="Mono sweep file")
    parser.add_argument("--input_device", type=str, default=None,
                        help="Input device name or number")
    parser.add_argument("--output_device", type=str, default=None,
                        help="Output device name or number")
    parser.add_argument("--host_api", type=str, default=None,
                        help="Preferred host API")
    args = parser.parse_args()

    layout_name, groups = select_layout(args.layout)
    init_layout(layout_name, groups, args.dir)

    run_capture(
        layout_name,
        groups,
        args.dir,
        stereo_sweep=args.stereo_sweep,
        mono_sweep=args.mono_sweep,
        input_device=args.input_device,
        output_device=args.output_device,
        host_api=args.host_api,
    )


if __name__ == "__main__":
    main()
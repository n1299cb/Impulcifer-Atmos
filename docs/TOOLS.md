# Helper Tools

This project ships with command line helpers for preparing capture folders and guiding the measurement process.

## Layout Preparation (`generate_layout.py`)

Use this script to create a capture directory containing the expected WAV files for a chosen speaker layout. Placeholder sweep recordings are copied into each file so you can verify channel order before doing the real measurements.

```bash
python generate_layout.py --layout=9.1.6 --dir=data/my_hrir
```

The script writes a short `README.md` describing all files. Run it with `--verify` to check for missing or unexpected WAVs. You can also store the selected speaker groups into a JSON preset with `--save_preset my_layout.json`. Use `--list` to print the available layouts and `--preset_file processing-presets.json` to load additional user presets.

## Capture Wizard (`capture_wizard.py`)

After creating the folder, `capture_wizard.py` walks you through recording each group. It plays the appropriate sweep (stereo or mono) and saves the recordings in sequence.

```bash
python capture_wizard.py --layout=9.1.6 --dir=data/my_hrir --input_device='USB mic' --output_device='DAC'
```

The wizard prompts you to insert the microphones, position for each speaker group and confirm when ready. Additional options let you choose the sweep files and host API.

Both tools can also be launched from the GUI: the **Layout Wizard** button on the *Setup* tab opens the layout helper, while the **Capture Wizard** button on the *Execution* tab starts the step-by-step recorder.

## Real-Time Convolver Benchmark (`benchmark_realtime_convolver.py`)

This small utility measures the processing throughput of the pure Python
`RealTimeConvolver` implementation. It uses synthetic impulse responses so
no measurement data is required. The benchmark repeatedly feeds random
blocks into the engine and reports the average time per block.

Run it with default settings:

```bash
python benchmark_realtime_convolver.py
```

Options allow controlling block size, impulse response length, sample rate,
the number of angles and how many blocks to process. A random seed can be set
for reproducible results:

```bash
python benchmark_realtime_convolver.py \
  --block_size=512 --ir_length=128 --samplerate=96000 \
  --angles=8 --blocks=2000 --seed=42
```

Use this tool to establish a performance baseline before experimenting with
SIMD or GPU optimizations.
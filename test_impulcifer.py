import os
import shutil
import numpy as np
from impulcifer import main
from hrir import HRIR
from impulse_response_estimator import ImpulseResponseEstimator
from constants import (
    APPLY_ROOM_CORRECTION,
    APPLY_HEADPHONE_EQ,
    APPLY_DIFFUSE_FIELD_COMPENSATION,
    PRESERVE_ROOM_RESPONSE
)

# === Configuration ===
test_dir = "data/test_capture"
cleanup = False
test_signal = None

# Full 9.1.6 speaker layout
speakers_916 = [
    "FL", "FR", "FC", "SL", "SR", "BL", "BR", "WL", "WR",
    "TFL", "TFR", "TSL", "TSR", "TBL", "TBR"
]

# === Cleanup
if cleanup and os.path.exists(test_dir):
    shutil.rmtree(test_dir)
os.makedirs(test_dir, exist_ok=True)

print("\n=== Impulcifer 9.1.6 Test Harness ===")
print(f"Room Correction:      {APPLY_ROOM_CORRECTION}")
print(f"Headphone EQ:         {APPLY_HEADPHONE_EQ}")
print(f"Diffuse-field EQ:     {APPLY_DIFFUSE_FIELD_COMPENSATION}")
print(f"Preserve Room IRs:    {PRESERVE_ROOM_RESPONSE}")

hrir_files = [f for f in os.listdir(test_dir) if f.lower().endswith(".wav")]
if not hrir_files:
    print("❌ No HRIR WAV files found.")
    exit(1)

print(f"✔ Found HRIR files: {', '.join(hrir_files)}")

# === Run processing pipeline
main(
    dir_path=test_dir,
    plot=True,
    do_room_correction=APPLY_ROOM_CORRECTION,
    do_headphone_compensation=APPLY_HEADPHONE_EQ,
    do_equalization=APPLY_DIFFUSE_FIELD_COMPENSATION,
    test_signal=test_signal,
    channel_balance="avg",
    fs=None
)

# === Validate output
output_path = os.path.join(test_dir, "responses.wav")
if not os.path.exists(output_path):
    print("❌ No output file generated.")
    exit(1)

print(f"\n📦 Inspecting output: {output_path}")
estimator = ImpulseResponseEstimator(fs=48000)
hrir = HRIR(estimator)
hrir.open_recording(output_path, speakers=speakers_916[:len(hrir.irs)])

for speaker, pair in hrir.irs.items():
    l_peak = np.max(pair["left"].data)
    r_peak = np.max(pair["right"].data)
    print(f"🔊 {speaker:4} | Left peak: {l_peak:.4f}, Right peak: {r_peak:.4f}")
    if l_peak < 1e-5 and r_peak < 1e-5:
        print(f"⚠️  WARNING: {speaker} appears silent or missing.")

print("\n✅ 9.1.6 Test complete.\n")

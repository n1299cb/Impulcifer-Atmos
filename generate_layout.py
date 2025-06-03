# generate_layout.py

import os
from constants import SPEAKER_LAYOUTS

# === Ask user for layout selection
print("🎧 Select speaker layout:")
layout_names = list(SPEAKER_LAYOUTS.keys())
for i, name in enumerate(layout_names, 1):
    print(f"{i}. {name}")

choice = input("\nEnter layout number: ")

try:
    layout_name = layout_names[int(choice) - 1]
    speaker_groups = SPEAKER_LAYOUTS[layout_name]
except (IndexError, ValueError):
    print("❌ Invalid selection.")
    exit(1)

# === Output paths
output_dir = "data/test_capture"
os.makedirs(output_dir, exist_ok=True)
readme_path = os.path.join(output_dir, "README.md")

# === Write expected layout to README
with open(readme_path, "w") as f:
    f.write(f"# HRIR Capture Layout: {layout_name}\n\n")
    f.write("## Expected Files:\n")
    for group in speaker_groups:
        filename = ",".join(group) + ".wav"
        f.write(f"- `{filename}` → {', '.join(group)}\n")
    f.write("\nMake sure each file contains properly labeled and measured IRs.\n")

print(f"\n✅ Layout `{layout_name}` selected.")
print(f"📄 Saved expected filenames to: {readme_path}")
print("💡 You may now begin your capture using `recorder.py`.\n")

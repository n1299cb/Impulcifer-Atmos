# EarprintGUI

EarprintGUI is a native macOS interface for the Earprint processing
pipeline. The Swift app bundles the Python scripts found in the
`Scripts` directory and executes them through an embedded Python
interpreter.  The repository cannot always ship the full Python
framework, so follow the steps below to add it to your build and
install the required dependencies.

## Embedding Python

1. Download a **Python 3.8–3.11** macOS installer from
   [python.org](https://www.python.org/downloads/macos/).  Versions
   3.8 through 3.11 are supported. The "macOS 64‑bit universal2 installer"
   installs `Python.framework` under `/Library/Frameworks`.
2. Copy the entire `Python.framework` directory into
   `EarprintGUI/Resources/EmbeddedPython` so the interpreter resides at
   `EarprintGUI/Resources/EmbeddedPython/Python.framework/Versions/<VERSION>/bin/python3`.
   Create a symlink `Versions/<VERSION> → <VERSION>.x` (replace `<VERSION>` with
   your installed minor version such as `3.9` or `3.11`).

```
cp -R /Library/Frameworks/Python.framework \
      EarprintGUI/Resources/EmbeddedPython/
```

## Installing Dependencies

Install the Python packages directly into the embedded interpreter. From
within your `Versions/<VERSION>` directory run:

```
cd EarprintGUI/Resources/EmbeddedPython/Python.framework/Versions/<VERSION>
./bin/python3 -m ensurepip --upgrade
./bin/pip3 install -r ../../../Scripts/requirements.txt
```

Additional optional packages (for example `pyfftw` for faster
convolution) can be installed the same way.

## Building the App

With the framework in place you can build and run the SwiftUI
application:

```
cd EarprintGUI
swift run
```

Open the project in Xcode if you prefer a GUI.  The app will launch the
Python scripts using the interpreter embedded in `Resources/EmbeddedPython`.
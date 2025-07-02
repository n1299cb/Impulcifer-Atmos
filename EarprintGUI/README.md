# EarprintGUI

EarprintGUI is a native macOS interface for the Earprint processing
pipeline. The Swift app bundles the Python scripts found in the
`Scripts` directory and executes them through an embedded Python
interpreter.  The repository cannot always ship the full Python
framework, so follow the steps below to add it to your build and
install the required dependencies.

## Embedding Python

1. Download the official **Python 3.9** macOS installer from
   [python.org](https://www.python.org/downloads/macos/).  The
   "macOS 64‑bit universal2 installer" installs
   `Python.framework` under `/Library/Frameworks`.
2. Copy the entire `Python.framework` directory into
   `EarprintGUI/Resources/EmbeddedPython` so the interpreter resides at
   `EarprintGUI/Resources/EmbeddedPython/Python.framework/Versions/3.9/bin/python3`.
   A symlink `Versions/3.9 → 3.9.x` is expected.

```
cp -R /Library/Frameworks/Python.framework \
      EarprintGUI/Resources/EmbeddedPython/
```

## Installing Dependencies

Install the Python packages directly into the embedded interpreter. From
within the `Versions/3.9` directory run:

```
cd EarprintGUI/Resources/EmbeddedPython/Python.framework/Versions/3.9
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
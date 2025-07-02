Copy the official macOS Python distribution into this directory. Versions 3.8 through 3.11 are supported.
The expected layout is:

EmbeddedPython
└── Python.framework
    └── Versions
        └── <VERSION> -> <VERSION>.x

Place the entire `Python.framework` folder from `/Library/Frameworks`
so that `bin/python3` resides at:
`EarprintGUI.app/Contents/Resources/EmbeddedPython/Python.framework/Versions/<VERSION>/bin/python3`.
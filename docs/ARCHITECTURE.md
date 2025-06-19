# Project Architecture

This code base follows a lightweight **Model–View–ViewModel (MVVM)** layout. High level components include:

- **Models (`models/`)** – simple data classes that capture user input and processing settings.
- **ViewModels (`viewmodel/`)** – orchestrate command line tools and validate data. They expose methods used by the GUI.
- **View (`gui.py`)** – Qt based interface that binds widgets to ViewModel commands.
- **Domain tools (`impulcifer.py`, `recorder.py`, etc.)** – processing logic called by ViewModels.

## Current State

The project largely adheres to MVVM. The GUI delegates recording and processing to the `RecordingViewModel` and `ProcessingViewModel`, while path validation is handled by `MeasurementSetupViewModel`. Unit tests exercise these view models to keep the interface layer free from heavy logic.

## Potential Improvements

- Move layout selection helpers (`generate_layout.py`) under a dedicated ViewModel to further decouple the GUI from command line utilities.
- Provide additional unit tests for `ProcessingViewModel` and `RecordingViewModel` to ensure command arguments are built correctly.
- Keep GUI modules focused on presentation by placing any new processing steps in a ViewModel or domain script.
- All processing modules should be properly separated and according to MVVM and isolated from the view/GUI section.
- When validating measurement or test signal paths, call
  `MeasurementSetupViewModel.validate_paths` rather than using `os.path`
  checks directly in the view layer.
- For simple file or directory checks, use the
  `MeasurementSetupViewModel.file_exists` and `directory_exists` helpers
  from the view layer.
- Global processing flags are consolidated in `config.py`. Import the
  `settings` object and adjust its attributes instead of editing scattered
  constants.
  
This document acts as a reference for contributors aiming to keep the MVVM separation intact.

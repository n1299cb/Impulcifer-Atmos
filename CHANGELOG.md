# Changelog
Here you'll find the history of changes. The version numbering complies with [SemVer]() system which means that when the
first number changes, something has broken and you need to check your commands and/or files, when the second number
changes there are only new features available and nothing old has broken and when the last number changes, old bugs have
been fixed and old features improved.

## 1.1.0 - 2025-06-17
This release represents the first public version of the Atmos fork. It was
forked from [Jaakko Pasanen's Impulcifer](https://github.com/jaakkopasanen/Impulcifer)
at tag `1.0.0` (`6817f62`). Major changes include:

### Added
- 7.1.4 and 9.1.6 speaker layouts.
- Layout preparation tools and an interactive layout wizard.
- Capture wizard for guided HRIR recording.
- Diffuse-field compensation and SMPTE X-Curve options.
- Support for per‑speaker delay tables via `--delay-file`.
- Additional context attributes for `DeviceNotFoundError` to aid debugging.
- Replacement of the original Tkinter GUI with a PySide6 interface built around
  a lightweight MVVM architecture.

## Unreleased
### Removed
- `APPLY_DIRECTIONAL_GAINS` constant from `constants.py` as it was unused.

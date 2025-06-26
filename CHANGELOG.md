# Changelog
Here you'll find the history of changes. The version numbering complies with [SemVer]() system which means that when the
first number changes, something has broken and you need to check your commands and/or files, when the second number
changes there are only new features available and nothing old has broken and when the last number changes, old bugs have
been fixed and old features improved.

## 1.1.0 - 2025-06-17
- Added 7.1.4 and 9.1.6 speaker layouts.
- Added layout preparation tools and layout wizard.
- Added capture wizard for guided HRIR recording.
- Added diffuse-field compensation and SMPTE X-Curve options.

### Added
- Support for per-speaker delay tables via `--delay-file`.

## Unreleased
### Removed
- `APPLY_DIRECTIONAL_GAINS` constant from `constants.py` as it was unused.

## 1.0.0 - 2020-07-20
Performance improvements. Main features are supported and Impulcifer is relatively stable.

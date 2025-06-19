# Development Guide

This short guide covers the typical workflow for contributors.

## Environment Setup

1. Create and activate a Python virtual environment.
2. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Adjust processing flags via `config.py` if required. The helper
   `settings.update()` accepts keyword arguments to toggle features.

## Running Tests

The project ships with simple regression tests. Execute them with
`pytest` to run everything at once:

```bash
pytest
```

Set the `IMPULCIFER_TEST_CAPTURE_DIR` environment variable to point to
real measurement data to skip synthetic samples.

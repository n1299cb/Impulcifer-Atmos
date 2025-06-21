import os
from viewmodel import MeasurementSetupViewModel


def test_validate_paths(tmp_path):
    vm = MeasurementSetupViewModel()

    # Non-existing paths should return both errors
    errors = vm.validate_paths('missing.wav', tmp_path / 'none')
    assert 'test_signal' in errors
    assert 'measurement_dir' in errors

    # Create valid paths
    signal = tmp_path / 'tone.wav'
    signal.write_text('data')
    errors = vm.validate_paths(str(signal), str(tmp_path))
    assert errors == []


def test_file_and_directory_checks(tmp_path):
    vm = MeasurementSetupViewModel()

    existing_file = tmp_path / "a.wav"
    existing_file.write_text("data")
    missing_file = tmp_path / "missing.wav"

    existing_dir = tmp_path / "d"
    existing_dir.mkdir()
    missing_dir = tmp_path / "missing"

    assert vm.file_exists(str(existing_file))
    assert not vm.file_exists(str(missing_file))

    assert vm.directory_exists(str(existing_dir))
    assert not vm.directory_exists(str(missing_dir))
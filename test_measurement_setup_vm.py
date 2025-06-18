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

import os
import importlib

import json

import pytest

# Set custom env var for layout file

def test_save_and_load_custom_layout(tmp_path, monkeypatch):
    preset_file = tmp_path / 'preset.json'
    monkeypatch.setenv('IMPULCIFER_LAYOUT_PRESETS', str(preset_file))
    import constants
    importlib.reload(constants)

    constants.save_user_layout_preset('test', [['FL'], ['FR']], str(preset_file))
    loaded = constants.load_user_layout_presets(str(preset_file))
    assert 'test' in loaded
    assert loaded['test'] == [['FL'], ['FR']]

    # Reload constants to ensure automatic inclusion
    importlib.reload(constants)
    assert 'test' in constants.SPEAKER_LAYOUTS

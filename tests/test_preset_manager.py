import importlib

import pytest


def test_save_and_load_preset(tmp_path, monkeypatch):
    preset_file = tmp_path / "presets.json"
    monkeypatch.setenv("EARPRINT_PRESETS", str(preset_file))
    import preset_manager
    importlib.reload(preset_manager)
    from models import ProcessingSettings

    settings = ProcessingSettings(measurement_dir="dir")
    preset_manager.save_preset("test", settings, str(preset_file))
    presets = preset_manager.load_presets(str(preset_file))
    assert "test" in presets
    assert presets["test"]["measurement_dir"] == "dir"

    preset_manager.delete_preset("test", str(preset_file))
    presets = preset_manager.load_presets(str(preset_file))
    assert presets == {}

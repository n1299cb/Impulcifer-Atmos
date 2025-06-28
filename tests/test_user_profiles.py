import importlib

import pytest


def test_save_and_load_profile(tmp_path, monkeypatch):
    profiles_file = tmp_path / "profiles.json"
    monkeypatch.setenv("EARPRINT_PROFILES", str(profiles_file))
    import user_profiles

    importlib.reload(user_profiles)
    from models import UserProfile

    profile = UserProfile(brir_dir="brirs", tracking_calibration="track.cal", output_routing=[0, 1], latency=128)
    user_profiles.save_profile("test", profile, str(profiles_file))
    profiles = user_profiles.load_profiles(str(profiles_file))
    assert "test" in profiles
    assert profiles["test"]["brir_dir"] == "brirs"

    user_profiles.delete_profile("test", str(profiles_file))
    profiles = user_profiles.load_profiles(str(profiles_file))
    assert profiles == {}
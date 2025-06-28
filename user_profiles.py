import os
import json
from dataclasses import asdict, is_dataclass
from typing import Dict, Any, Union

from models import UserProfile

PROFILES_FILE = os.environ.get("IMPULCIFER_PROFILES", "profiles.json")


def load_profiles(file_path: str = PROFILES_FILE) -> Dict[str, Dict[str, Any]]:
    """Load user profiles from ``file_path``."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if isinstance(v, dict)}
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def save_profile(
    name: str,
    profile: Union[UserProfile, Dict[str, Any]],
    file_path: str = PROFILES_FILE,
) -> None:
    """Save ``profile`` under ``name``."""
    profiles = load_profiles(file_path)
    if is_dataclass(profile):
        profiles[name] = asdict(profile)
    else:
        profiles[name] = dict(profile)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)


def delete_profile(name: str, file_path: str = PROFILES_FILE) -> None:
    """Remove profile ``name`` from the file."""
    profiles = load_profiles(file_path)
    if name in profiles:
        del profiles[name]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2)
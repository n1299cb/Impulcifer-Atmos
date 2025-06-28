import os
import json
from dataclasses import asdict, is_dataclass
from typing import Dict, Any, Union

from models import ProcessingSettings

PRESETS_FILE = os.environ.get("EARPRINT_PRESETS", "presets.json")


def load_presets(file_path: str = PRESETS_FILE) -> Dict[str, Dict[str, Any]]:
    """Load processing presets from ``file_path``."""
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


def save_preset(
    name: str,
    settings: Union[ProcessingSettings, Dict[str, Any]],
    file_path: str = PRESETS_FILE,
) -> None:
    """Save ``settings`` under ``name``."""
    presets = load_presets(file_path)
    if is_dataclass(settings):
        presets[name] = asdict(settings)
    else:
        presets[name] = dict(settings)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=2)


def delete_preset(name: str, file_path: str = PRESETS_FILE) -> None:
    """Remove preset ``name`` from the file."""
    presets = load_presets(file_path)
    if name in presets:
        del presets[name]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2)

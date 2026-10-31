"""JSON settings persistence helpers with explicit paths and no import-time I/O.

The application continues to own its defaults and UI state.
"""
import json
from pathlib import Path
from typing import Any


def read_settings(path: Path, defaults: dict[str, Any]) -> dict[str, Any]:
    """Preserve legacy behavior: return any valid JSON object, else defaults."""
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return defaults


def write_settings(path: Path, settings: dict[str, Any]) -> None:
    """Write the same indented JSON format used by the legacy application."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2), encoding="utf-8")

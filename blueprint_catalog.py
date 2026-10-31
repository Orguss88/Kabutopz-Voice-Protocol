"""Versioned, external blueprint catalog with strict shape validation."""
import json
from pathlib import Path


def load_blueprint_catalog(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Unsupported blueprint catalog schema")
    entries = data.get("blueprints")
    if not isinstance(entries, list):
        raise ValueError("blueprints must be a list")
    ids = set()
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("Blueprint entries must be objects")
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in ids:
            raise ValueError("Blueprint IDs must be unique nonempty strings")
        ids.add(identifier)
        if not isinstance(item.get("name"), str) or not item["name"].strip():
            raise ValueError("Blueprint names must be nonempty strings")
    return data

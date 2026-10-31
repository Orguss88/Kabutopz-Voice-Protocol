"""Settings tests use only temporary paths, never real user settings."""
import ast
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from settings_store import read_settings, write_settings


class SettingsStoreTests(unittest.TestCase):
    def test_missing_returns_defaults(self):
        with TemporaryDirectory() as directory:
            defaults = {"voice_feedback": True, "keybinds": {}}
            self.assertEqual(read_settings(Path(directory) / "missing.json", defaults), defaults)

    def test_round_trip_preserves_unknown_fields(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "settings.json"
            data = {"tts_volume": 80, "keybinds": {"quantum_engage": "b"}, "future_setting": [1, 2]}
            write_settings(path, data)
            self.assertEqual(read_settings(path, {}), data)
            self.assertIn("\n  \"tts_volume\"", path.read_text(encoding="utf-8"))

    def test_corrupt_json_falls_back(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text("{bad", encoding="utf-8")
            self.assertEqual(read_settings(path, {"theme": "default"}), {"theme": "default"})

    def test_non_object_json_falls_back(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text("[]", encoding="utf-8")
            self.assertEqual(read_settings(path, {"voice_feedback": True}), {"voice_feedback": True})

    def test_existing_object_not_merged_with_defaults(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text('{"tts_voice":"Test"}', encoding="utf-8")
            self.assertEqual(read_settings(path, {"voice_feedback": True}), {"tts_voice": "Test"})

    def test_app_delegates_to_settings_store(self):
        source = (Path(__file__).resolve().parents[1] / "starcitizen_voice_keybinds.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = {
            alias.name for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "settings_store"
            for alias in node.names
        }
        self.assertTrue({"read_settings", "write_settings"} <= imported)


if __name__ == "__main__":
    unittest.main()

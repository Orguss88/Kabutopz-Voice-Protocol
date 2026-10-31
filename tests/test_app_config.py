"""Configuration tests never read or modify the user's settings."""
import ast
from pathlib import Path
import re
import unittest

import app_config


class AppConfigTests(unittest.TestCase):
    def test_version(self):
        self.assertRegex(app_config.APP_VERSION, r"^\d+\.\d+(?:\.\d+)?$")

    def test_settings_location_unchanged(self):
        self.assertEqual(app_config.APP_DIR, Path.home() / ".star_citizen_voice_keybinds")
        self.assertEqual(app_config.SETTINGS_FILE, app_config.APP_DIR / "settings.json")

    def test_audio_capture_defaults(self):
        self.assertEqual(app_config.COMMAND_SAMPLE_RATE, 16000)
        self.assertEqual(app_config.COMMAND_PREROLL_CHUNKS, 8)
        self.assertGreater(app_config.COMMAND_MAX_CAPTURE_SECONDS, app_config.COMMAND_END_SILENCE_SECONDS)

    def test_page_order(self):
        self.assertEqual(app_config.PAGE_ORDER[0], "VOICE PROTOCOL")
        self.assertIn("ANNOUNCEMENTS", app_config.PAGE_ORDER)

    def test_application_imports_shared_configuration(self):
        source = (Path(__file__).resolve().parents[1] / "starcitizen_voice_keybinds.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        names = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "app_config"
            for alias in node.names
        }
        self.assertTrue({"APP_VERSION", "SETTINGS_FILE", "COMMAND_SAMPLE_RATE", "PAGE_ORDER"} <= names)
        assigned = {
            target.id
            for node in tree.body if isinstance(node, (ast.Assign, ast.AnnAssign))
            for target in (node.targets if isinstance(node, ast.Assign) else [node.target])
            if isinstance(target, ast.Name)
        }
        self.assertFalse(names & assigned)


if __name__ == "__main__":
    unittest.main()

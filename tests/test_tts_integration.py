"""Static TTS integration test: never import the app or start speech."""
import ast
from pathlib import Path
import unittest


class TTSIntegrationTests(unittest.TestCase):
    def test_app_delegates_to_tts_builders(self):
        source = (Path(__file__).resolve().parents[1] / "starcitizen_voice_keybinds.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = {
            alias.name
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "tts_service"
            for alias in node.names
        }
        self.assertTrue({"build_speech_script", "build_voice_listing_script"} <= imported)
        app = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "VoiceKeybindApp")
        for method_name, builder in (
            ("_speak", "build_speech_script"),
            ("_refresh_tts_voices", "build_voice_listing_script"),
        ):
            method = next(node for node in app.body if isinstance(node, ast.FunctionDef) and node.name == method_name)
            calls = [
                node for node in ast.walk(method)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            ]
            self.assertEqual(sum(call.func.id == builder for call in calls), 1)


if __name__ == "__main__":
    unittest.main()

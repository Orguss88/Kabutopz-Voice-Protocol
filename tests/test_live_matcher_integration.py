"""Static integration contract: no GUI/audio import and no key injection."""
import ast
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "starcitizen_voice_keybinds.py"


class LiveMatcherIntegrationTests(unittest.TestCase):
    def test_live_matcher_delegates_to_pure_function(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        imports = [
            node for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "phrase_matcher"
        ]
        self.assertTrue(
            any(any(alias.name == "build_phrase_pairs" for alias in node.names) for node in imports)
        )
        app_class = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "VoiceKeybindApp"
        )
        method = next(
            node for node in app_class.body
            if isinstance(node, ast.FunctionDef) and node.name == "_build_phrase_matcher"
        )
        self.assertEqual(len(method.body), 1)
        result = method.body[0]
        self.assertIsInstance(result, ast.Return)
        self.assertIsInstance(result.value, ast.Call)
        self.assertIsInstance(result.value.func, ast.Name)
        self.assertEqual(result.value.func.id, "build_phrase_pairs")
        self.assertEqual(len(result.value.args), 1)
        self.assertIsInstance(result.value.args[0], ast.Attribute)
        self.assertEqual(result.value.args[0].attr, "phrases")


if __name__ == "__main__":
    unittest.main()

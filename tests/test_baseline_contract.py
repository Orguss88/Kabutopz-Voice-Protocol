"""Read-only baseline tests: never instantiate the UI or send input."""
import ast
from pathlib import Path
import unittest

from app_config import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "starcitizen_voice_keybinds.py"


def load_constants():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    assignments = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"ACTIONS", "DEFAULT_PHRASES"}:
                    assignments[target.id] = ast.literal_eval(node.value)
    return assignments


class BaselineContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.values = load_constants()

    def test_action_registry_exists(self):
        self.assertTrue(self.values["ACTIONS"])

    def test_action_types_are_supported(self):
        supported = {"tap", "hold", "wheel", "combo_mouse"}
        for action_id, action in self.values["ACTIONS"].items():
            with self.subTest(action=action_id):
                self.assertIn(action["type"], supported)
                self.assertTrue(action["key"])
                if action["type"] == "hold":
                    self.assertIsInstance(action["hold"], (int, float))
                    self.assertGreater(action["hold"], 0)

    def test_default_phrases_reference_known_actions(self):
        actions = self.values["ACTIONS"]
        for action_id, phrases in self.values["DEFAULT_PHRASES"].items():
            with self.subTest(action=action_id):
                self.assertIn(action_id, actions)
                self.assertIsInstance(phrases, list)
                for phrase in phrases:
                    self.assertIsInstance(phrase, str)
                    self.assertTrue(phrase.strip())

    def test_critical_actions_have_expected_default_keys(self):
        actions = self.values["ACTIONS"]
        self.assertEqual(actions["quit_star_citizen"]["key"], "alt+f4")
        self.assertEqual(actions["self_destruct"]["type"], "hold")
        self.assertEqual(actions["self_destruct"]["key"], "backspace")
        self.assertEqual(actions["quantum_engage"]["type"], "hold")

    def test_app_version_is_declared(self):
        self.assertRegex(APP_VERSION, r"^\d+\.\d+(?:\.\d+)?$")


if __name__ == "__main__":
    unittest.main()

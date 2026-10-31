"""Static integration checks; do not import the GUI or win_input."""
import ast
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "starcitizen_voice_keybinds.py"


class CommandRouterIntegrationTests(unittest.TestCase):
    def test_run_action_delegates_to_router(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        imports = [
            node for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "command_router"
        ]
        imported = {alias.name for node in imports for alias in node.names}
        self.assertTrue({"Command", "execute_command"} <= imported)
        app = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "VoiceKeybindApp")
        method = next(n for n in app.body if isinstance(n, ast.FunctionDef) and n.name == "_run_action")
        self.assertEqual([arg.arg for arg in method.args.args], ["action_type", "key", "hold_seconds"])
        calls = [
            node for node in ast.walk(method)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        ]
        self.assertEqual(sum(node.func.id == "execute_command" for node in calls), 1)
        self.assertEqual(sum(node.func.id == "Command" for node in calls), 1)
        for name in ("tap_keybind", "hold_keybind", "scroll_wheel", "tap_mouse_combo"):
            self.assertFalse(any(node.func.id == name for node in calls))


if __name__ == "__main__":
    unittest.main()

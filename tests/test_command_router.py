"""CommandRouter tests use only fake handlers; never send real input."""
import unittest
from command_router import Command, execute_command, plan_command


class CommandRouterTests(unittest.TestCase):
    def test_plan_tap_is_pure(self):
        actions = {"gear": {"type": "tap", "key": "n", "hold": None}}
        self.assertEqual(plan_command("gear", actions), Command("gear", "tap", "n", None))

    def test_plan_self_destruct_hold(self):
        actions = {"self_destruct": {"type": "hold", "key": "backspace", "hold": 1.5}}
        command = plan_command("self_destruct", actions)
        self.assertEqual((command.action_type, command.hold_seconds), ("hold", 1.5))

    def test_unknown_action_rejected(self):
        with self.assertRaises(KeyError):
            plan_command("missing", {})

    def test_invalid_hold_rejected(self):
        with self.assertRaises(ValueError):
            plan_command("bad", {"bad": {"type": "hold", "key": "y", "hold": 0}})

    def test_unsupported_action_rejected(self):
        with self.assertRaises(ValueError):
            plan_command("bad", {"bad": {"type": "launch", "key": "x"}})

    def test_execution_uses_fake_tap_handler(self):
        calls = []
        execute_command(Command("gear", "tap", "n", None), {"tap": lambda key: calls.append(("tap", key))})
        self.assertEqual(calls, [("tap", "n")])

    def test_execution_uses_fake_hold_handler(self):
        calls = []
        execute_command(Command("self_destruct", "hold", "backspace", 1.5), {"hold": lambda key, seconds: calls.append((key, seconds))})
        self.assertEqual(calls, [("backspace", 1.5)])

    def test_missing_handler_never_falls_back_to_real_input(self):
        with self.assertRaises(KeyError):
            execute_command(Command("gear", "tap", "n", None), {})


if __name__ == "__main__":
    unittest.main()

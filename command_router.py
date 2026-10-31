"""Pure command planning and opt-in execution with injectable input handlers.

Importing or planning commands never sends keyboard/mouse events.
"""
from dataclasses import dataclass
from typing import Callable, Mapping


@dataclass(frozen=True)
class Command:
    action_id: str
    action_type: str
    key: str
    hold_seconds: float | None


def plan_command(action_id: str, actions: Mapping[str, dict]) -> Command:
    """Resolve an action without performing side effects."""
    action = actions[action_id]
    action_type = action["type"]
    if action_type not in {"tap", "hold", "wheel", "combo_mouse"}:
        raise ValueError(f"Unsupported action type: {action_type}")
    key = action["key"]
    if not isinstance(key, str) or not key.strip():
        raise ValueError("Action key must be a nonempty string")
    hold = action.get("hold")
    if action_type == "hold" and (not isinstance(hold, (int, float)) or isinstance(hold, bool) or hold <= 0):
        raise ValueError("Hold action requires a positive duration")
    return Command(action_id, action_type, key, hold)


def execute_command(command: Command, handlers: Mapping[str, Callable]) -> None:
    """Execute only via caller-supplied handlers (mock these in tests)."""
    handler = handlers[command.action_type]
    if command.action_type == "hold":
        handler(command.key, command.hold_seconds)
    else:
        handler(command.key)

"""Shared, side-effect-free application configuration.

Settings remain in the same user directory; importing this module never writes files.
"""
from pathlib import Path

APP_VERSION = "1.5"
APP_DIR = Path.home() / ".star_citizen_voice_keybinds"
SETTINGS_FILE = APP_DIR / "settings.json"
COOLDOWN_SECONDS = 1.5
COMMAND_SAMPLE_RATE = 16000
COMMAND_VOICE_THRESHOLD = 450
COMMAND_TRAILING_VOICE_THRESHOLD = 160
COMMAND_END_SILENCE_SECONDS = 0.45
COMMAND_MAX_CAPTURE_SECONDS = 3.2
COMMAND_PREROLL_CHUNKS = 8
PAGE_ORDER = (
    "VOICE PROTOCOL", "HOW TO", "CUSTOMIZE", "PHRASES", "KEYBINDS",
    "CUSTOM WORDS", "COMPONENTS", "SHIP WEAPONS", "COMMODITIES", "MINING MODE", "SHIP FINDER",
    "GUIDES", "ANNOUNCEMENTS", "CREDIT",
)

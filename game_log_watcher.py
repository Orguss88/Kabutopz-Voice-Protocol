"""Offline-first incremental Game.log reader.

Event patterns are caller-provided until verified against real Star Citizen logs.
No filesystem polling threads, UI, or game process are started on import.
"""
from dataclasses import dataclass
from pathlib import Path
import os
import re


@dataclass(frozen=True)
class LogEvent:
    kind: str
    raw: str
    recognized: bool


def classify_line(line: str, patterns: dict[str, str] | None = None) -> LogEvent:
    """Classify using explicit regex rules; unmatched lines remain visible."""
    for kind, pattern in (patterns or {}).items():
        if re.search(pattern, line):
            return LogEvent(kind, line, True)
    return LogEvent("unknown", line, False)


class GameLogWatcher:
    """Poll a path incrementally; emit complete lines once, including offline replay.

    A new file identity or a shorter file resets the offset and partial buffer.
    Read bytes to avoid splitting multi-byte UTF-8 characters between polls.
    """

    def __init__(self, path: str | Path, patterns: dict[str, str] | None = None):
        self.path = Path(path)
        self.patterns = dict(patterns or {})
        self.offset = 0
        self._identity = None
        self._pending = b""

    def reset(self):
        self.offset = 0
        self._identity = None
        self._pending = b""

    def poll(self) -> list[LogEvent]:
        try:
            with self.path.open("rb") as stream:
                stat = os.fstat(stream.fileno())
                identity = (stat.st_dev, stat.st_ino)
                if self._identity != identity or stat.st_size < self.offset:
                    self.offset = 0
                    self._pending = b""
                self._identity = identity
                stream.seek(self.offset)
                chunk = stream.read()
                self.offset = stream.tell()
        except FileNotFoundError:
            self.reset()
            return []

        if not chunk:
            return []
        segments = (self._pending + chunk).split(b"\n")
        self._pending = segments.pop()
        return [
            classify_line(segment.rstrip(b"\r").decode("utf-8", errors="replace"), self.patterns)
            for segment in segments
        ]

    def replay(self) -> list[LogEvent]:
        """Replay from the beginning without altering the watcher's live offset."""
        reader = GameLogWatcher(self.path, self.patterns)
        return reader.poll()

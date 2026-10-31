import tempfile
from pathlib import Path
import unittest

from game_log_watcher import GameLogWatcher, classify_line


class GameLogWatcherTests(unittest.TestCase):
    def test_unknown_and_recognized(self):
        self.assertFalse(classify_line("unmapped").recognized)
        event = classify_line("TEST_EVENT: mission", {"test_event": r"^TEST_EVENT:"})
        self.assertEqual((event.kind, event.recognized), ("test_event", True))

    def test_partial_lines_and_append(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Game.log"
            path.write_bytes(b"first\nsecond")
            watcher = GameLogWatcher(path)
            self.assertEqual([e.raw for e in watcher.poll()], ["first"])
            self.assertEqual(watcher.poll(), [])
            with path.open("ab") as stream:
                stream.write(b" half\nthird\n")
            self.assertEqual([e.raw for e in watcher.poll()], ["second half", "third"])

    def test_truncation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Game.log"
            path.write_text("original line\n", encoding="utf-8")
            watcher = GameLogWatcher(path)
            self.assertEqual(len(watcher.poll()), 1)
            path.write_text("new\n", encoding="utf-8")
            self.assertEqual([e.raw for e in watcher.poll()], ["new"])

    def test_rotation_by_rename(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Game.log"
            path.write_text("old\n", encoding="utf-8")
            watcher = GameLogWatcher(path)
            watcher.poll()
            path.rename(Path(folder) / "Game.old.log")
            path.write_text("fresh\n", encoding="utf-8")
            self.assertEqual([e.raw for e in watcher.poll()], ["fresh"])

    def test_missing_then_created(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Game.log"
            watcher = GameLogWatcher(path)
            self.assertEqual(watcher.poll(), [])
            path.write_text("ready\n", encoding="utf-8")
            self.assertEqual([e.raw for e in watcher.poll()], ["ready"])

    def test_replay_does_not_change_position(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Game.log"
            path.write_text("one\ntwo\n", encoding="utf-8")
            watcher = GameLogWatcher(path)
            self.assertEqual(len(watcher.poll()), 2)
            self.assertEqual(len(watcher.replay()), 2)
            self.assertEqual(watcher.poll(), [])

    def test_split_utf8(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "Game.log"
            watcher = GameLogWatcher(path)
            with path.open("wb") as stream:
                stream.write("café".encode("utf-8")[:-1])
            self.assertEqual(watcher.poll(), [])
            with path.open("ab") as stream:
                stream.write("café".encode("utf-8")[-1:] + b"\n")
            self.assertEqual(watcher.poll()[0].raw, "café")


if __name__ == "__main__":
    unittest.main()

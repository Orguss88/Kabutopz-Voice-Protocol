"""TTS tests only inspect strings; never start PowerShell or audio."""
import unittest
from tts_service import build_speech_script, build_voice_listing_script


class TTSServiceTests(unittest.TestCase):
    def test_default_voice(self):
        script = build_speech_script("Hello", 65, "Windows Default Voice")
        self.assertIn("$s.Volume = 65", script)
        self.assertIn("$s.Speak('Hello')", script)
        self.assertNotIn("SelectVoice", script)

    def test_custom_voice(self):
        self.assertIn("SelectVoice('Test Voice')", build_speech_script("Hi", 50, "Test Voice"))

    def test_quotes_are_escaped(self):
        script = build_speech_script("Pilot's ready", 50, "Captain's Voice")
        self.assertIn("Pilot''s ready", script)
        self.assertIn("Captain''s Voice", script)

    def test_volume_clamped(self):
        self.assertIn("$s.Volume = 100", build_speech_script("Hi", 200, ""))
        self.assertIn("$s.Volume = 0", build_speech_script("Hi", -20, ""))

    def test_voice_listing(self):
        self.assertIn("GetInstalledVoices()", build_voice_listing_script())


if __name__ == "__main__":
    unittest.main()

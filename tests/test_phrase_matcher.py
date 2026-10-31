"""Pure regression tests; these never import the GUI or send input."""
import unittest

from phrase_matcher import build_phrase_pairs, first_matching_action


class PhraseMatcherTests(unittest.TestCase):
    def test_longest_phrase_first(self):
        pairs = build_phrase_pairs({"short": ["power on"], "long": ["ship power on"]})
        self.assertEqual(pairs[0], ("ship power on", "long"))

    def test_equal_length_preserves_registry_order(self):
        pairs = build_phrase_pairs({"first": ["alpha"], "second": ["bravo"]})
        self.assertEqual(pairs, [("alpha", "first"), ("bravo", "second")])

    def test_substring_behavior_is_preserved(self):
        self.assertEqual(
            first_matching_action("please ship power on now", {"power": ["ship power on"]}, {}, 100, 1),
            ("ship power on", "power"),
        )

    def test_cooldown_skips_action_and_tries_next(self):
        phrases = {"a": ["engines on"], "b": ["on"]}
        self.assertEqual(
            first_matching_action("engines on", phrases, {"a": 99.5}, 100, 1),
            ("on", "b"),
        )

    def test_no_match(self):
        self.assertIsNone(first_matching_action("hello", {"a": ["gear down"]}, {}, 100, 1))

    def test_matcher_has_no_side_effects(self):
        phrases = {"a": ["landing gear"]}
        last = {"a": 20}
        first_matching_action("landing gear", phrases, last, 100, 1)
        self.assertEqual(phrases, {"a": ["landing gear"]})
        self.assertEqual(last, {"a": 20})


if __name__ == "__main__":
    unittest.main()

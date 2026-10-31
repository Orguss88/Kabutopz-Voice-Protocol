"""Pure phrase matching extracted from the existing listener's ordering rules.

No audio, GUI, network, or keyboard input is performed by this module.
"""
from collections.abc import Mapping, Sequence


def build_phrase_pairs(phrases: Mapping[str, Sequence[str]]) -> list[tuple[str, str]]:
    """Return (phrase, action_id) ordered longest first, preserving ties.

    This reproduces the current application's _build_phrase_matcher behavior.
    It intentionally does not change substring matching semantics yet.
    """
    pairs = [
        (phrase, action_id)
        for action_id, alternatives in phrases.items()
        for phrase in alternatives
    ]
    pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
    return pairs


def first_matching_action(
    heard: str,
    phrases: Mapping[str, Sequence[str]],
    last_triggered: Mapping[str, float],
    now: float,
    cooldown_seconds: float,
) -> tuple[str, str] | None:
    """Match the first non-cooled-down phrase using legacy substring rules."""
    for phrase, action_id in build_phrase_pairs(phrases):
        if phrase in heard and now - last_triggered.get(action_id, 0) >= cooldown_seconds:
            return phrase, action_id
    return None

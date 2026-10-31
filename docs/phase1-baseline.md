# Phase 1 — safe baseline

This branch begins the September core-foundation roadmap. These tests intentionally
do not import the Windows input layer, initialize Tkinter, access microphones,
start speech recognition, contact game-data services, or transmit keybinds.

## Run locally (Surface Pro 9 / PowerShell)

```powershell
py -m compileall -q .
py -m unittest discover -s tests -p "test_*.py" -v
```

The CI workflow runs the same tests on Windows with Python 3.11 and 3.12.
It does not install audio dependencies because these AST-based contract tests
do not import the application.

## Next tasks

1. Capture current matching behavior with isolated tests.
2. Extract PhraseMatcher and CommandRouter with injectable, mocked input.
3. Extract Windows TTS into a service and add subprocess mocks.
4. Test settings validation and atomic writes.
5. Run manual microphone and Star Citizen input checks separately.

Do not interpret passing static baseline tests as successful microphone,
Windows SendInput, or in-game integration testing.

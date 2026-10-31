"""Pure Windows System.Speech PowerShell command construction.

No speech or subprocess starts when importing or calling these builders.
"""


def _ps_quote(value: str) -> str:
    return str(value).replace("'", "''")


def build_speech_script(phrase: str, volume: int, voice: str) -> str:
    volume = max(0, min(100, int(volume)))
    voice = voice.strip()
    select = ""
    if voice and voice != "Windows Default Voice":
        select = f"try {{ $s.SelectVoice('{_ps_quote(voice)}') }} catch {{ }}; "
    return (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Volume = {volume}; "
        f"{select}"
        f"$s.Speak('{_ps_quote(phrase)}')"
    )


def build_voice_listing_script() -> str:
    return (
        "Add-Type -AssemblyName System.Speech; "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }"
    )

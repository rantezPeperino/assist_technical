from __future__ import annotations

from pathlib import Path

from voice_agent.config.settings import Settings
from voice_agent.domain.ports.speech_to_text import SpeechToTextPort


class TranscribeAudioUseCase:
    def __init__(self, speech_to_text: SpeechToTextPort) -> None:
        self._speech_to_text = speech_to_text

    def execute(self, audio_path: Path, settings: Settings) -> str:
        return self._speech_to_text.transcribe(
            audio_path=audio_path,
            model=settings.stt_model,
            language=settings.stt_language or None,
            prompt=settings.stt_prompt or None,
        )
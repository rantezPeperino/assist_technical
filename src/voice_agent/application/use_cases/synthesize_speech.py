from __future__ import annotations

from pathlib import Path

from voice_agent.config.settings import Settings
from voice_agent.domain.ports.text_to_speech import TextToSpeechPort
from voice_agent.infrastructure.system.file_system import ensure_directory


class SynthesizeSpeechUseCase:
    def __init__(self, text_to_speech: TextToSpeechPort) -> None:
        self._text_to_speech = text_to_speech

    def execute(
        self,
        text: str,
        output_path: Path,
        settings: Settings,
    ) -> Path:
        ensure_directory(settings.tts_output_dir)
        return self._text_to_speech.synthesize(
            text=text,
            output_path=output_path,
            model=settings.tts_model,
            voice=settings.tts_voice,
            response_format=settings.tts_format,
            instructions=settings.tts_instructions,
        )
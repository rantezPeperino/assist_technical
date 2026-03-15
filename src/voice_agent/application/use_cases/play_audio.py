from __future__ import annotations

from pathlib import Path

from voice_agent.config.settings import Settings
from voice_agent.domain.ports.audio_output import AudioOutputPort


class PlayAudioUseCase:
    def __init__(self, audio_output: AudioOutputPort) -> None:
        self._audio_output = audio_output

    def execute(self, audio_path: Path, settings: Settings) -> None:
        self._audio_output.play(
            audio_path=audio_path,
            output_device=settings.output_device,
        )
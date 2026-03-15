from __future__ import annotations

from voice_agent.config.settings import Settings
from voice_agent.domain.models.audio_models import AudioRecording
from voice_agent.domain.ports.audio_input import AudioInputPort
from voice_agent.infrastructure.audio.local_file_audio_repository import (
    LocalFileAudioRepository,
)


class RecordAudioUseCase:
    def __init__(
        self,
        audio_input: AudioInputPort,
        audio_repository: LocalFileAudioRepository,
    ) -> None:
        self._audio_input = audio_input
        self._audio_repository = audio_repository

    def execute(self, settings: Settings) -> AudioRecording:
        output_path = self._audio_repository.next_recording_path()
        return self._audio_input.record(
            output_path=output_path,
            duration_seconds=settings.record_seconds,
            sample_rate=settings.sample_rate,
            channels=settings.channels,
            sample_format=settings.sample_format,
            input_device=settings.input_device,
        )
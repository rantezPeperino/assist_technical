from __future__ import annotations

from pathlib import Path

from voice_agent.application.use_cases.play_audio import PlayAudioUseCase
from voice_agent.application.use_cases.record_audio import RecordAudioUseCase
from voice_agent.application.use_cases.synthesize_speech import SynthesizeSpeechUseCase
from voice_agent.application.use_cases.transcribe_audio import TranscribeAudioUseCase
from voice_agent.application.use_cases.voice_pipeline import (
    VoicePipelineResult,
    VoicePipelineUseCase,
)
from voice_agent.config.settings import Settings
from voice_agent.domain.models.audio_models import AudioRecording


class MvpOrchestrator:
    def __init__(
        self,
        record_audio_use_case: RecordAudioUseCase,
        play_audio_use_case: PlayAudioUseCase,
        transcribe_audio_use_case: TranscribeAudioUseCase | None = None,
        synthesize_speech_use_case: SynthesizeSpeechUseCase | None = None,
        voice_pipeline_use_case: VoicePipelineUseCase | None = None,
    ) -> None:
        self._record_audio_use_case = record_audio_use_case
        self._play_audio_use_case = play_audio_use_case
        self._transcribe_audio_use_case = transcribe_audio_use_case
        self._synthesize_speech_use_case = synthesize_speech_use_case
        self._voice_pipeline_use_case = voice_pipeline_use_case

    def run_stage_one(self, settings: Settings) -> AudioRecording:
        recording = self._record_audio_use_case.execute(settings)
        self._play_audio_use_case.execute(recording.path, settings)
        return recording

    def run_stage_two(self, settings: Settings) -> tuple[AudioRecording, str]:
        if self._transcribe_audio_use_case is None:
            raise RuntimeError("TranscribeAudioUseCase no está configurado.")

        recording = self._record_audio_use_case.execute(settings)
        transcription = self._transcribe_audio_use_case.execute(recording.path, settings)
        return recording, transcription

    def run_stage_four(self, settings: Settings) -> VoicePipelineResult:
        if self._voice_pipeline_use_case is None:
            raise RuntimeError("VoicePipelineUseCase no está configurado.")
        return self._voice_pipeline_use_case.execute(settings)

    def record_only(self, settings: Settings) -> AudioRecording:
        return self._record_audio_use_case.execute(settings)

    def play_file(self, audio_path: Path, settings: Settings) -> None:
        self._play_audio_use_case.execute(audio_path, settings)

    def transcribe_file(self, audio_path: Path, settings: Settings) -> str:
        if self._transcribe_audio_use_case is None:
            raise RuntimeError("TranscribeAudioUseCase no está configurado.")
        return self._transcribe_audio_use_case.execute(audio_path, settings)

    def synthesize_text(
        self,
        text: str,
        output_path: Path,
        settings: Settings,
    ) -> Path:
        if self._synthesize_speech_use_case is None:
            raise RuntimeError("SynthesizeSpeechUseCase no está configurado.")
        return self._synthesize_speech_use_case.execute(text, output_path, settings)
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from voice_agent.application.use_cases.play_audio import PlayAudioUseCase
from voice_agent.application.use_cases.record_audio import RecordAudioUseCase
from voice_agent.application.use_cases.synthesize_speech import SynthesizeSpeechUseCase
from voice_agent.application.use_cases.transcribe_audio import TranscribeAudioUseCase
from voice_agent.config.settings import Settings
from voice_agent.domain.models.audio_models import AudioRecording
from voice_agent.domain.ports.language_model import LanguageModelPort
from voice_agent.infrastructure.system.file_system import build_tts_output_path


@dataclass(frozen=True)
class VoicePipelineResult:
    recording: AudioRecording
    transcription: str
    llm_response: str
    generated_audio_path: Path


class VoicePipelineUseCase:
    def __init__(
        self,
        record_audio_use_case: RecordAudioUseCase,
        transcribe_audio_use_case: TranscribeAudioUseCase,
        language_model: LanguageModelPort,
        synthesize_speech_use_case: SynthesizeSpeechUseCase,
        play_audio_use_case: PlayAudioUseCase,
    ) -> None:
        self._record_audio_use_case = record_audio_use_case
        self._transcribe_audio_use_case = transcribe_audio_use_case
        self._language_model = language_model
        self._synthesize_speech_use_case = synthesize_speech_use_case
        self._play_audio_use_case = play_audio_use_case

    def execute(self, settings: Settings) -> VoicePipelineResult:
        recording = self._record_audio_use_case.execute(settings)

        transcription = self._transcribe_audio_use_case.execute(
            recording.path,
            settings,
        )

        llm_response = self._language_model.ask(
            user_text=transcription,
            system_prompt=settings.system_prompt,
            model=settings.llm_model,
            max_output_tokens=settings.max_output_tokens,
        )

        output_path = build_tts_output_path(
            settings.tts_output_dir,
            settings.tts_format,
        )

        generated_audio_path = self._synthesize_speech_use_case.execute(
            text=llm_response,
            output_path=output_path,
            settings=settings,
        )

        self._play_audio_use_case.execute(
            generated_audio_path,
            settings,
        )

        return VoicePipelineResult(
            recording=recording,
            transcription=transcription,
            llm_response=llm_response,
            generated_audio_path=generated_audio_path,
        )
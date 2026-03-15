from __future__ import annotations

import argparse
from pathlib import Path
from subprocess import CompletedProcess

from voice_agent.application.orchestrators.mvp_orchestrator import MvpOrchestrator
from voice_agent.application.use_cases.play_audio import PlayAudioUseCase
from voice_agent.application.use_cases.record_audio import RecordAudioUseCase
from voice_agent.application.use_cases.synthesize_speech import SynthesizeSpeechUseCase
from voice_agent.application.use_cases.transcribe_audio import TranscribeAudioUseCase
from voice_agent.application.use_cases.voice_pipeline import VoicePipelineUseCase
from voice_agent.config.settings import Settings
from voice_agent.infrastructure.ai.openai.openai_llm import OpenAiLanguageModelAdapter
from voice_agent.infrastructure.ai.openai.openai_stt import OpenAiSpeechToTextAdapter
from voice_agent.infrastructure.ai.openai.openai_tts import OpenAiTextToSpeechAdapter
from voice_agent.infrastructure.audio.local_file_audio_repository import (
    LocalFileAudioRepository,
)
from voice_agent.infrastructure.audio.respeaker_audio_io import (
    RespeakerAudioInput,
    RespeakerAudioOutput,
)
from voice_agent.infrastructure.system.file_system import build_tts_output_path
from voice_agent.infrastructure.system.shell_audio_utils import (
    ShellCommandError,
    require_command,
    run_command,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voice-agent",
        description="Voice Agent MVP - Etapas 1, 2, 3 y 4",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("run-stage1", help="Graba y luego reproduce el audio grabado")
    subparsers.add_parser("run-stage2", help="Graba y luego transcribe el audio")
    subparsers.add_parser("run-stage4", help="Ejecuta el flujo completo del agente de voz")
    subparsers.add_parser("record", help="Solo graba audio")
    subparsers.add_parser("list-devices", help="Lista dispositivos ALSA")

    play_parser = subparsers.add_parser("play", help="Reproduce un archivo de audio")
    play_parser.add_argument("--file", required=True, help="Ruta del archivo")

    transcribe_parser = subparsers.add_parser(
        "transcribe", help="Transcribe un archivo de audio con OpenAI"
    )
    transcribe_parser.add_argument("--file", required=True, help="Ruta del archivo de audio")

    synthesize_parser = subparsers.add_parser(
        "synthesize", help="Convierte texto en archivo de audio con OpenAI TTS"
    )
    synthesize_parser.add_argument("--text", required=True, help="Texto a sintetizar")

    return parser


def build_orchestrator(settings: Settings) -> MvpOrchestrator:
    audio_input = RespeakerAudioInput()
    audio_output = RespeakerAudioOutput()
    audio_repository = LocalFileAudioRepository(settings.recordings_dir)

    record_audio = RecordAudioUseCase(
        audio_input=audio_input,
        audio_repository=audio_repository,
    )
    play_audio = PlayAudioUseCase(audio_output=audio_output)

    transcribe_audio = None
    synthesize_speech = None
    voice_pipeline = None

    if settings.openai_api_key:
        stt_adapter = OpenAiSpeechToTextAdapter(api_key=settings.openai_api_key)
        tts_adapter = OpenAiTextToSpeechAdapter(api_key=settings.openai_api_key)
        llm_adapter = OpenAiLanguageModelAdapter(api_key=settings.openai_api_key)

        transcribe_audio = TranscribeAudioUseCase(speech_to_text=stt_adapter)
        synthesize_speech = SynthesizeSpeechUseCase(text_to_speech=tts_adapter)

        voice_pipeline = VoicePipelineUseCase(
            record_audio_use_case=record_audio,
            transcribe_audio_use_case=transcribe_audio,
            language_model=llm_adapter,
            synthesize_speech_use_case=synthesize_speech,
            play_audio_use_case=play_audio,
        )

    return MvpOrchestrator(
        record_audio_use_case=record_audio,
        play_audio_use_case=play_audio,
        transcribe_audio_use_case=transcribe_audio,
        synthesize_speech_use_case=synthesize_speech,
        voice_pipeline_use_case=voice_pipeline,
    )


def list_devices() -> tuple[CompletedProcess[str], CompletedProcess[str]]:
    require_command("arecord")
    require_command("aplay")

    capture_devices = run_command(["arecord", "-l"])
    playback_devices = run_command(["aplay", "-l"])
    return capture_devices, playback_devices


def run_cli() -> None:
    parser = build_parser()
    args = parser.parse_args()
    settings = Settings.from_env()
    orchestrator = build_orchestrator(settings)

    try:
        if args.command == "list-devices":
            capture_devices, playback_devices = list_devices()
            print("=== Dispositivos de captura ===")
            print(capture_devices.stdout.strip() or "(sin salida)")
            print()
            print("=== Dispositivos de reproducción ===")
            print(playback_devices.stdout.strip() or "(sin salida)")
            return

        if args.command == "record":
            recording = orchestrator.record_only(settings)
            print("Grabación finalizada")
            print(f"Archivo: {recording.path}")
            return

        if args.command == "play":
            audio_path = Path(args.file)
            if not audio_path.exists():
                raise FileNotFoundError(f"No existe el archivo: {audio_path}")
            orchestrator.play_file(audio_path, settings)
            print(f"Reproducción finalizada: {audio_path}")
            return

        if args.command == "transcribe":
            audio_path = Path(args.file)
            if not audio_path.exists():
                raise FileNotFoundError(f"No existe el archivo: {audio_path}")
            transcription = orchestrator.transcribe_file(audio_path, settings)
            print("=== Transcripción ===")
            print(transcription)
            return

        if args.command == "synthesize":
            output_path = build_tts_output_path(
                settings.tts_output_dir,
                settings.tts_format,
            )
            generated_file = orchestrator.synthesize_text(
                text=args.text,
                output_path=output_path,
                settings=settings,
            )
            print("=== Audio generado ===")
            print(generated_file)
            return

        if args.command == "run-stage1":
            print("Iniciando grabación...")
            recording = orchestrator.run_stage_one(settings)
            print("Flujo etapa 1 completado")
            print(f"Archivo generado: {recording.path}")
            return

        if args.command == "run-stage2":
            print("Iniciando grabación...")
            recording, transcription = orchestrator.run_stage_two(settings)
            print("Flujo etapa 2 completado")
            print(f"Archivo generado: {recording.path}")
            print("=== Transcripción ===")
            print(transcription)
            return

        if args.command == "run-stage4":
            print("Iniciando flujo completo del agente de voz...")
            result = orchestrator.run_stage_four(settings)
            print("Flujo etapa 4 completado")
            print(f"Audio grabado: {result.recording.path}")
            print("=== Transcripción ===")
            print(result.transcription)
            print("=== Respuesta del agente ===")
            print(result.llm_response)
            print(f"Audio generado: {result.generated_audio_path}")
            return

    except (ShellCommandError, FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1) from exc
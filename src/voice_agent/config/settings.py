from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    input_device: str = "default"
    output_device: str = "default"
    sample_rate: int = 16000
    channels: int = 1
    sample_format: str = "S16_LE"
    record_seconds: int = 5
    recordings_dir: Path = Path("data/recordings")

    openai_api_key: str = ""
    stt_model: str = "gpt-4o-mini-transcribe"
    stt_language: str = "es"
    stt_prompt: str = ""

    tts_model: str = "gpt-4o-mini-tts"
    tts_voice: str = "alloy"
    tts_format: str = "wav"
    tts_instructions: str = ""
    tts_output_dir: Path = Path("data/generated_audio")

    llm_model: str = "gpt-4o-mini"
    system_prompt: str = (
        "Eres un asistente de voz breve, claro y útil. "
        "Responde en español de forma natural."
    )
    max_output_tokens: int = 200

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            input_device=os.getenv("VOICE_AGENT_INPUT_DEVICE", "default"),
            output_device=os.getenv("VOICE_AGENT_OUTPUT_DEVICE", "default"),
            sample_rate=int(os.getenv("VOICE_AGENT_SAMPLE_RATE", "16000")),
            channels=int(os.getenv("VOICE_AGENT_CHANNELS", "1")),
            sample_format=os.getenv("VOICE_AGENT_SAMPLE_FORMAT", "S16_LE"),
            record_seconds=int(os.getenv("VOICE_AGENT_RECORD_SECONDS", "5")),
            recordings_dir=Path(
                os.getenv("VOICE_AGENT_RECORDINGS_DIR", "data/recordings")
            ),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            stt_model=os.getenv("VOICE_AGENT_STT_MODEL", "gpt-4o-mini-transcribe"),
            stt_language=os.getenv("VOICE_AGENT_STT_LANGUAGE", "es"),
            stt_prompt=os.getenv("VOICE_AGENT_STT_PROMPT", ""),
            tts_model=os.getenv("VOICE_AGENT_TTS_MODEL", "gpt-4o-mini-tts"),
            tts_voice=os.getenv("VOICE_AGENT_TTS_VOICE", "alloy"),
            tts_format=os.getenv("VOICE_AGENT_TTS_FORMAT", "wav"),
            tts_instructions=os.getenv("VOICE_AGENT_TTS_INSTRUCTIONS", ""),
            tts_output_dir=Path(
                os.getenv("VOICE_AGENT_TTS_OUTPUT_DIR", "data/generated_audio")
            ),
            llm_model=os.getenv("VOICE_AGENT_LLM_MODEL", "gpt-4o-mini"),
            system_prompt=os.getenv(
                "VOICE_AGENT_SYSTEM_PROMPT",
                "Eres un asistente de voz breve, claro y útil. "
                "Responde en español de forma natural.",
            ),
            max_output_tokens=int(
                os.getenv("VOICE_AGENT_MAX_OUTPUT_TOKENS", "200")
            ),
        )
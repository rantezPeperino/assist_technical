from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from voice_agent.domain.ports.speech_to_text import SpeechToTextPort


class OpenAiSpeechToTextAdapter(SpeechToTextPort):
    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY no está configurada.")
        self._client = OpenAI(api_key=api_key)

    def transcribe(
        self,
        audio_path: Path,
        model: str,
        language: str | None = None,
        prompt: str | None = None,
    ) -> str:
        if not audio_path.exists():
            raise FileNotFoundError(f"No existe el archivo de audio: {audio_path}")

        with audio_path.open("rb") as audio_file:
            transcription = self._client.audio.transcriptions.create(
                file=audio_file,
                model=model,
                language=language,
                prompt=prompt,
            )

        text = getattr(transcription, "text", None)
        if not text:
            raise RuntimeError("La respuesta de transcripción no devolvió texto.")
        return text.strip()
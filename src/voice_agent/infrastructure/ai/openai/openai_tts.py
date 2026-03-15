from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from voice_agent.domain.ports.text_to_speech import TextToSpeechPort


class OpenAiTextToSpeechAdapter(TextToSpeechPort):
    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY no está configurada.")
        self._client = OpenAI(api_key=api_key)

    def synthesize(
        self,
        text: str,
        output_path: Path,
        model: str,
        voice: str,
        response_format: str,
        instructions: str | None = None,
    ) -> Path:
        if not text or not text.strip():
            raise ValueError("El texto a sintetizar no puede estar vacío.")

        payload = {
            "model": model,
            "voice": voice,
            "input": text.strip(),
            "response_format": response_format,
        }

        if instructions is not None and instructions.strip():
            payload["instructions"] = instructions.strip()

        with self._client.audio.speech.with_streaming_response.create(
            **payload
        ) as response:
            response.stream_to_file(output_path)

        if not output_path.exists():
            raise RuntimeError(
                f"No se generó el archivo de salida esperado: {output_path}"
            )

        return output_path
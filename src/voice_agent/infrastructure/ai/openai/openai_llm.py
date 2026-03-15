from __future__ import annotations

from openai import OpenAI

from voice_agent.domain.ports.language_model import LanguageModelPort


class OpenAiLanguageModelAdapter(LanguageModelPort):
    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY no está configurada.")
        self._client = OpenAI(api_key=api_key)

    def ask(
        self,
        user_text: str,
        system_prompt: str,
        model: str,
        max_output_tokens: int,
    ) -> str:
        if not user_text or not user_text.strip():
            raise ValueError("El texto del usuario no puede estar vacío.")

        response = self._client.responses.create(
            model=model,
            instructions=system_prompt,
            input=user_text.strip(),
            max_output_tokens=max_output_tokens,
        )

        output_text = getattr(response, "output_text", None)
        if output_text and output_text.strip():
            return output_text.strip()

        raise RuntimeError("El modelo no devolvió texto en la respuesta.")
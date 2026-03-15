from __future__ import annotations

from typing import Protocol


class LanguageModelPort(Protocol):
    def ask(
        self,
        user_text: str,
        system_prompt: str,
        model: str,
        max_output_tokens: int,
    ) -> str:
        ...
from __future__ import annotations

from pathlib import Path
from typing import Protocol


class SpeechToTextPort(Protocol):
    def transcribe(
        self,
        audio_path: Path,
        model: str,
        language: str | None = None,
        prompt: str | None = None,
    ) -> str:
        ...
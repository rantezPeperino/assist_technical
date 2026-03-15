from __future__ import annotations

from pathlib import Path
from typing import Protocol


class TextToSpeechPort(Protocol):
    def synthesize(
        self,
        text: str,
        output_path: Path,
        model: str,
        voice: str,
        response_format: str,
        instructions: str | None = None,
    ) -> Path:
        ...
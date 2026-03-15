from __future__ import annotations

from pathlib import Path
from typing import Protocol


class AudioOutputPort(Protocol):
    def play(self, audio_path: Path, output_device: str) -> None:
        ...
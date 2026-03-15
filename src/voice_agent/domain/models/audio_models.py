from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AudioRecording:
    path: Path
    sample_rate: int
    channels: int
    sample_format: str
    duration_seconds: int
    input_device: str
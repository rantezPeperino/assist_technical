from __future__ import annotations

from pathlib import Path
from typing import Protocol

from voice_agent.domain.models.audio_models import AudioRecording


class AudioInputPort(Protocol):
    def record(
        self,
        output_path: Path,
        duration_seconds: int,
        sample_rate: int,
        channels: int,
        sample_format: str,
        input_device: str,
    ) -> AudioRecording:
        ...
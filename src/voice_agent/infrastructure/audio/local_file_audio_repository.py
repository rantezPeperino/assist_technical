from __future__ import annotations

from pathlib import Path

from voice_agent.infrastructure.system.file_system import build_recording_path


class LocalFileAudioRepository:
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir

    def next_recording_path(self) -> Path:
        return build_recording_path(self._base_dir)
from __future__ import annotations

from datetime import datetime
from pathlib import Path


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_recording_path(base_dir: Path) -> Path:
    ensure_directory(base_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return base_dir / f"recording_{timestamp}.wav"


def build_tts_output_path(base_dir: Path, extension: str) -> Path:
    ensure_directory(base_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    normalized_extension = extension.lower().lstrip(".")
    return base_dir / f"tts_{timestamp}.{normalized_extension}"
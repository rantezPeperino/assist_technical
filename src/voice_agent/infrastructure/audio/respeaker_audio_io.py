from __future__ import annotations

from pathlib import Path

from voice_agent.domain.models.audio_models import AudioRecording
from voice_agent.domain.ports.audio_input import AudioInputPort
from voice_agent.domain.ports.audio_output import AudioOutputPort
from voice_agent.infrastructure.system.shell_audio_utils import (
    require_command,
    run_command,
)


class RespeakerAudioInput(AudioInputPort):
    def record(
        self,
        output_path: Path,
        duration_seconds: int,
        sample_rate: int,
        channels: int,
        sample_format: str,
        input_device: str,
    ) -> AudioRecording:
        require_command("arecord")

        command = [
            "arecord",
            "-D",
            input_device,
            "-t",
            "wav",
            "-d",
            str(duration_seconds),
            "-r",
            str(sample_rate),
            "-c",
            str(channels),
            "-f",
            sample_format,
            str(output_path),
        ]
        run_command(command)

        return AudioRecording(
            path=output_path,
            sample_rate=sample_rate,
            channels=channels,
            sample_format=sample_format,
            duration_seconds=duration_seconds,
            input_device=input_device,
        )


class RespeakerAudioOutput(AudioOutputPort):
    def play(self, audio_path: Path, output_device: str) -> None:
        require_command("aplay")

        command = [
            "aplay",
            "-D",
            output_device,
            str(audio_path),
        ]
        run_command(command)
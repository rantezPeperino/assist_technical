from __future__ import annotations

import shutil
import subprocess
from typing import Sequence


class ShellCommandError(RuntimeError):
    pass


def require_command(command_name: str) -> None:
    if shutil.which(command_name) is None:
        raise ShellCommandError(
            f"No se encontró el comando '{command_name}'. "
            f"Instalá alsa-utils y verificá que esté en PATH."
        )


def run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else ""
        stdout = exc.stdout.strip() if exc.stdout else ""
        details = stderr or stdout or "sin detalle adicional"
        raise ShellCommandError(
            f"Falló el comando: {' '.join(command)}\nDetalle: {details}"
        ) from exc
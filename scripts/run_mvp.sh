#!/usr/bin/env bash
set -eu pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
fi

if [[ -f ".env" ]]; then
  set -a
  source .env
  set +a
fi

python -m voice_agent.main run
#!/usr/bin/env bash
set -euo pipefail

TEST_FILE="${1:-/tmp/voice_agent_smoke_test.wav}"
DURATION="${2:-3}"
INPUT_DEVICE="${VOICE_AGENT_INPUT_DEVICE:-default}"
OUTPUT_DEVICE="${VOICE_AGENT_OUTPUT_DEVICE:-default}"

echo "=== Dispositivos de captura ==="
arecord -l || true
echo
echo "=== Dispositivos de reproducción ==="
aplay -l || true
echo

echo "Grabando ${DURATION}s en ${TEST_FILE}..."
arecord -D "${INPUT_DEVICE}" -t wav -d "${DURATION}" -r 16000 -c 1 -f S16_LE "${TEST_FILE}"

echo "Reproduciendo ${TEST_FILE}..."
aplay -D "${OUTPUT_DEVICE}" "${TEST_FILE}"

echo "Smoke test OK"
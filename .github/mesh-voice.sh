#!/usr/bin/env bash
# Fetches the voice mesh-check.py reads with into ./voice, from Piper's voices list at the commit MESH pins
# (PiperDownload.VoicesCommit in MESH), so a check uses the voice files MESH's users get.
set -euo pipefail
commit=e9ab671f2a0e50a701b34361136ba3e6a3a9eb0c
base="https://huggingface.co/rhasspy/piper-voices/resolve/$commit/en/en_GB/alba/medium"
mkdir -p voice
curl -sSfL -o voice/en_GB-alba-medium.onnx "$base/en_GB-alba-medium.onnx"
curl -sSfL -o voice/en_GB-alba-medium.onnx.json "$base/en_GB-alba-medium.onnx.json"

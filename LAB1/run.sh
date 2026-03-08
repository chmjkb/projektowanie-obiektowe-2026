#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Building Docker image..."
docker build -t pascal-lab1 "$SCRIPT_DIR"

echo ""
echo "=== Running main program ==="
docker run --rm -v "$SCRIPT_DIR:/app" pascal-lab1 \
  bash -c "fpc main.pas && echo '' && ./main"

echo ""
echo "=== Running unit tests ==="
docker run --rm -v "$SCRIPT_DIR:/app" pascal-lab1 \
  bash -c "fpc tests.pas && echo '' && ./tests --all"

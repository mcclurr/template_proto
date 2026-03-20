#!/usr/bin/env bash
set -e

# Resolve project root (works from anywhere)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Set PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/src:$PROJECT_ROOT/src/protos:$PYTHONPATH"

# Run the app (forward all args)
exec python "$PROJECT_ROOT/src/main.py" "$@"
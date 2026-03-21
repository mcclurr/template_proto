#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"

if [ -x "$VENV_PYTHON" ]; then
  PYTHON_BIN="$VENV_PYTHON"
else
  PYTHON_BIN="python"
fi

export PYTHONPATH="$PROJECT_ROOT/src:$PROJECT_ROOT/generated:$PYTHONPATH"

exec "$PYTHON_BIN" "$PROJECT_ROOT/src/main.py" "$@"
#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"

echo "Project root: $PROJECT_ROOT"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing requirements..."
pip install -r "$PROJECT_ROOT/requirements.txt"

echo "Generating protobuf Python files..."
"$PROJECT_ROOT/scripts/gen_protos.sh"

echo "Setup complete."
echo "Run with: $PROJECT_ROOT/scripts/run.sh"
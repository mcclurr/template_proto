#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GENERATED_DIR="$PROJECT_ROOT/generated"
PROTOS_DIR="$PROJECT_ROOT/protos"

mkdir -p "$GENERATED_DIR"

find "$GENERATED_DIR" -type f -name "*_pb2.py" -delete

python -m grpc_tools.protoc \
  -I "$PROTOS_DIR" \
  --python_out="$GENERATED_DIR" \
  $(find "$PROTOS_DIR" -name "*.proto")

echo "Generated protobuf Python files in $GENERATED_DIR"
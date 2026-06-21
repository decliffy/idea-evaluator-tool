#!/usr/bin/env bash
# Builds the Lambda deployment package into infra/build/lambda using Docker so
# that compiled dependencies (pydantic-core, jiter) ship as Linux x86_64 wheels
# matching the Lambda runtime. Terraform then zips infra/build/lambda.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
BUILD_DIR="$SCRIPT_DIR/build/lambda"

echo ">> Cleaning $BUILD_DIR"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo ">> Installing dependencies via amazonlinux/Lambda python3.13 image"
docker run --rm --platform linux/amd64 \
  -v "$BACKEND_DIR:/src:ro" \
  -v "$BUILD_DIR:/out" \
  --entrypoint /bin/bash \
  public.ecr.aws/lambda/python:3.13 \
  -c "pip install --no-cache-dir -r /src/requirements-lambda.txt -t /out"

echo ">> Copying application source"
cp "$BACKEND_DIR/main.py" "$BUILD_DIR/"
cp "$BACKEND_DIR/evaluator.py" "$BUILD_DIR/"

echo ">> Pruning build artifacts"
find "$BUILD_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$BUILD_DIR" -type d -name "*.dist-info" -prune -exec rm -rf {} +
find "$BUILD_DIR" -type d -name "tests" -prune -exec rm -rf {} +

echo ">> Build complete: $BUILD_DIR"
du -sh "$BUILD_DIR"

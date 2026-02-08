#!/usr/bin/env bash
# Render build script

set -o errexit  # Exit on error

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Build complete!"

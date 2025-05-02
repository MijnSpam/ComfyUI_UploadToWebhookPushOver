#!/bin/bash

echo "🔧 Installing dependencies for ComfyUI_UploadToWebHook..."

# Exit immediately if a command exits with a non-zero status
set -e

# Activate venv if in ComfyUI RunPod or similar
if [ -d "../../venv" ]; then
    echo "📦 Activating virtual environment..."
    source ../../venv/bin/activate
fi

# Install requirements
pip install -r requirements.txt

echo "✅ Installation complete!"

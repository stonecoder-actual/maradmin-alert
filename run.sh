#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set virtual environment path
VENV_PATH="$SCRIPT_DIR/venv"
PYTHON_EXE="$VENV_PATH/bin/python"
PIP_EXE="$VENV_PATH/bin/pip"

echo "[$(date)] Starting maradmin-alert script..."

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "[$(date)] Virtual environment not found. Creating new environment..."
    python3 -m venv "$VENV_PATH"
    if [ $? -ne 0 ]; then
        echo "[$(date)] ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "[$(date)] Virtual environment created successfully"
fi

# Check if Python executable exists in venv
if [ ! -f "$PYTHON_EXE" ]; then
    echo "[$(date)] ERROR: Python executable not found in virtual environment"
    exit 1
fi

# Install/update requirements
echo "[$(date)] Installing/updating requirements..."
"$PIP_EXE" install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[$(date)] WARNING: Some packages may have failed to install"
fi

# Run the main script
echo "[$(date)] Running main.py..."
"$PYTHON_EXE" main.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date)] Script completed successfully"
else
    echo "[$(date)] Script failed with exit code $EXIT_CODE"
fi

echo "[$(date)] Finished"
exit $EXIT_CODE

#!/bin/bash
set -e

# Install Rust for tiktoken
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Source cargo environment
. "$HOME/.cargo/env"

# Add cargo to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Initialize pyenv if available
if [ -d "$HOME/.pyenv" ]; then
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
    # Try to initialize pyenv
    if [ -f "$PYENV_ROOT/bin/pyenv" ]; then
        eval "$($PYENV_ROOT/bin/pyenv init -)" || true
    fi
    # Also add common pyenv Python versions to PATH
    if [ -d "$PYENV_ROOT/versions" ]; then
        for pyver in "$PYENV_ROOT/versions"/*/bin; do
            if [ -d "$pyver" ]; then
                export PATH="$pyver:$PATH"
            fi
        done
    fi
fi

# Find Python - try multiple methods
PYTHON=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON=$(command -v python3)
elif command -v python >/dev/null 2>&1; then
    PYTHON=$(command -v python)
elif [ -f "/root/.pyenv/versions/3.9.16/bin/python3" ]; then
    PYTHON="/root/.pyenv/versions/3.9.16/bin/python3"
elif [ -f "/usr/bin/python3" ]; then
    PYTHON="/usr/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    PYTHON="/usr/local/bin/python3"
elif [ -f "/usr/bin/python" ]; then
    PYTHON="/usr/bin/python"
else
    # Try to find python3 or python in common locations
    PYTHON=$(find /usr -name python3 2>/dev/null | head -1)
    if [ -z "$PYTHON" ]; then
        PYTHON=$(find /usr -name python 2>/dev/null | head -1)
    fi
fi

# Verify Python was found
if [ -z "$PYTHON" ] || [ ! -f "$PYTHON" ]; then
    echo "Error: Python not found!"
    echo "Searching for Python..."
    which python3 || echo "python3 not in PATH"
    which python || echo "python not in PATH"
    find /usr -name python* 2>/dev/null | head -5 || echo "python not found in /usr"
    echo "PATH: $PATH"
    exit 1
fi

echo "Using Python: $PYTHON"
$PYTHON --version || $PYTHON -V

# Upgrade pip
$PYTHON -m pip install --upgrade pip setuptools wheel || pip install --upgrade pip setuptools wheel

# Install dependencies
$PYTHON -m pip install -r requirements.txt || pip install -r requirements.txt


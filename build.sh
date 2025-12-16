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
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)" || true
fi

# Find Python
PYTHON=$(command -v python3 || find /usr -name python3 2>/dev/null | head -1 || echo python3)

# Upgrade pip
$PYTHON -m pip install --upgrade pip setuptools wheel

# Install dependencies
$PYTHON -m pip install -r requirements.txt


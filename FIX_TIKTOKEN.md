# Fix tiktoken Build Error

## Problem
`tiktoken` requires Rust compiler to build from source, but Rust is not available in the build environment.

## Solution Options

### Option 1: Install Rust in Build Command (Recommended)

Update your build command in App Runner to:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && source $HOME/.cargo/env && python3 -m pip install --upgrade pip setuptools wheel && python3 -m pip install -r requirements.txt
```

### Option 2: Use Pre-built Wheel (Simpler)

Update build command to ensure pip is latest and use pre-built wheels:

```bash
python3 -m pip install --upgrade pip setuptools wheel && python3 -m pip install --only-binary :all: -r requirements.txt || python3 -m pip install -r requirements.txt
```

### Option 3: Make tiktoken Optional

If tiktoken isn't critical, you can make it optional in requirements.txt or remove it temporarily.

## Recommended Fix

Use Option 1 - Install Rust in the build command. This ensures tiktoken can build successfully.


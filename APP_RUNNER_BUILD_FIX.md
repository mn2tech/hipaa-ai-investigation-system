# App Runner Build Fix - Use Build Script

## Problem
Build command is too complex and App Runner is failing with "Check command syntax" error, even though packages install successfully.

## Solution: Use Build Script

I've created `build.sh` that App Runner can execute directly.

### Option 1: Use Build Script (Recommended)

**In App Runner Console:**

1. Edit service → Build & deploy → Edit build configuration
2. **Build command:**
   ```bash
   bash build.sh
   ```
3. **Start command:**
   ```bash
   python3 -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   ```
4. **Port:** `8000`
5. Save and redeploy

### Option 2: Simplified Inline Command

If build script doesn't work, try this simpler command:

**Build command:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y; . "$HOME/.cargo/env"; python3 -m pip install --upgrade pip setuptools wheel; python3 -m pip install -r requirements.txt
```

**Note:** Using `;` instead of `&&` - this continues even if one command fails (but should work fine)

### Option 3: Two-Step Build

Split into two commands:

**Build command:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
```

**Post-build command (if available):**
```bash
. "$HOME/.cargo/env" && python3 -m pip install --upgrade pip setuptools wheel && python3 -m pip install -r requirements.txt
```

## Why This Should Work

- Build script is simpler and easier for App Runner to parse
- All packages are already installing successfully
- The issue is just command syntax parsing
- Using `bash build.sh` is cleaner than inline complex commands

## After Pushing build.sh

1. Commit the build script:
   ```bash
   git add build.sh
   git commit -m "Add build script for App Runner"
   git push origin main
   ```

2. Update App Runner build command to: `bash build.sh`

3. Redeploy


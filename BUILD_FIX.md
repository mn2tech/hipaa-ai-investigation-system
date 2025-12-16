# Fix Build Error in AWS App Runner

## Problem
Build is failing with: "Failed to execute 'build' command"

## Root Cause
You're using Python 3.11 runtime, but the build commands may not be working correctly.

## Solution 1: Switch to Docker Runtime (RECOMMENDED)

### Steps:
1. Go to AWS App Runner Console
2. Find your service: `hipaa-investigation-system`
3. Click on the service name
4. Click "Edit" button (top right)
5. Go to "Build & deploy" section
6. Click "Edit" on Build configuration
7. Change **Runtime** from "Python 3.11" to **"Docker"**
8. App Runner will automatically detect your `Dockerfile`
9. Click "Save"
10. It will automatically redeploy

### Why Docker is Better:
- ✅ Uses your existing Dockerfile
- ✅ No need to configure build/start commands
- ✅ More reliable
- ✅ Matches your local environment

## Solution 2: Fix Python Build Commands

If you must use Python runtime, update these commands:

### In App Runner Console:
1. Edit your service
2. Go to "Build & deploy" → "Build configuration"
3. Update:

**Build command:**
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

**Start command:**
```bash
cd / && uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

**Port:** `8000`

## Solution 3: Use apprunner.yaml Configuration File

I've created `apprunner.yaml` in your repo. To use it:

1. In App Runner, go to "Configure build"
2. Select **"Use a configuration file"** (instead of "Configure all settings here")
3. App Runner will automatically use `apprunner.yaml`
4. Redeploy

## Quick Fix Steps:

1. **Edit Service** → **Build & deploy** → **Edit build configuration**
2. **Change Runtime to "Docker"**
3. **Save and redeploy**

This should fix the build error immediately!


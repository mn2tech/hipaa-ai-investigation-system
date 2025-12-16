# Git Setup on EC2

## Step 1: Check if git is installed

```bash
git --version
```

If not installed:
```bash
# For RHEL/CentOS/Amazon Linux
sudo yum install git -y

# For Ubuntu/Debian
sudo apt-get install git -y
```

## Step 2: Configure git (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Navigate to project directory

```bash
cd ~/hipaa-ai-investigation-system
```

## Step 4: Check current status

```bash
git status
```

## Step 5: Add and commit the build.sh file

```bash
# Add the build script
git add build.sh

# Commit
git commit -m "Add build script for App Runner"

# Push to GitHub
git push origin main
```

## If you get authentication errors

### Option A: Use Personal Access Token (Recommended)

1. Generate a token on GitHub:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control)
   - Copy the token

2. When pushing, use the token as password:
   ```bash
   git push origin main
   # Username: your-github-username
   # Password: paste-your-token-here
   ```

### Option B: Set up SSH key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
# Press Enter to accept default location
# Press Enter for no passphrase (or set one)

# View public key
cat ~/.ssh/id_ed25519.pub

# Copy the output and add to GitHub:
# https://github.com/settings/keys
# Click "New SSH key"
# Paste the key and save

# Test connection
ssh -T git@github.com
```

Then change remote URL to SSH:
```bash
git remote set-url origin git@github.com:mn2tech/hipaa-ai-investigation-system.git
```

## Quick Commands Summary

```bash
# Navigate to project
cd ~/hipaa-ai-investigation-system

# Check what files changed
git status

# Add build.sh
git add build.sh

# Commit
git commit -m "Add build script for App Runner"

# Push
git push origin main
```

## If you need to pull latest changes first

```bash
cd ~/hipaa-ai-investigation-system
git pull origin main
```

## Verify the push worked

Check on GitHub:
- Go to: https://github.com/mn2tech/hipaa-ai-investigation-system
- You should see `build.sh` in the repository


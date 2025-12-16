# Running on EC2 - Production Setup

## Option 1: Run as Background Process (Simple)

### Start the service in background:

```bash
cd ~/hipaa-ai-investigation-system

# Set environment variables
export OPENAI_API_KEY="your-actual-api-key"
export SECRET_KEY="dev-secret-key-change-in-production"
export ENCRYPTION_KEY="dev-encryption-key-change-in-production"
export DATABASE_URL="sqlite:///./investigation.db"
export DEBUG=False

# Run in background with nohup
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

# Check if it's running
ps aux | grep uvicorn

# View logs
tail -f app.log
```

### Stop the service:

```bash
# Find the process
ps aux | grep uvicorn

# Kill it
kill <PID>

# Or kill all uvicorn processes
pkill -f uvicorn
```

## Option 2: Run as Systemd Service (Recommended for Production)

### Step 1: Create systemd service file

```bash
sudo nano /etc/systemd/system/hipaa-ai.service
```

### Step 2: Add this content:

```ini
[Unit]
Description=HIPAA AI Investigation System
After=network.target

[Service]
Type=simple
User=raj
WorkingDirectory=/home/raj/hipaa-ai-investigation-system
Environment="OPENAI_API_KEY=your-actual-api-key"
Environment="SECRET_KEY=dev-secret-key-change-in-production"
Environment="ENCRYPTION_KEY=dev-encryption-key-change-in-production"
Environment="DATABASE_URL=sqlite:///./investigation.db"
Environment="DEBUG=False"
ExecStart=/usr/bin/python3 -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Important:** Replace `your-actual-api-key` with your real OpenAI API key!

### Step 3: Reload systemd and start service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start the service
sudo systemctl start hipaa-ai

# Enable to start on boot
sudo systemctl enable hipaa-ai

# Check status
sudo systemctl status hipaa-ai

# View logs
sudo journalctl -u hipaa-ai -f
```

### Step 4: Service management commands

```bash
# Start
sudo systemctl start hipaa-ai

# Stop
sudo systemctl stop hipaa-ai

# Restart
sudo systemctl restart hipaa-ai

# Status
sudo systemctl status hipaa-ai

# View logs
sudo journalctl -u hipaa-ai -f

# View recent logs
sudo journalctl -u hipaa-ai -n 50
```

## Option 3: Use Screen or Tmux (Good for Development)

### Using Screen:

```bash
# Install screen (if not installed)
sudo yum install screen -y  # For RHEL/CentOS
# or
sudo apt-get install screen -y  # For Ubuntu

# Start a new screen session
screen -S hipaa-ai

# Set environment variables
export OPENAI_API_KEY="your-actual-api-key"
export SECRET_KEY="dev-secret-key-change-in-production"
export ENCRYPTION_KEY="dev-encryption-key-change-in-production"
export DATABASE_URL="sqlite:///./investigation.db"
export DEBUG=False

# Navigate to project
cd ~/hipaa-ai-investigation-system

# Start the service
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Detach: Press Ctrl+A, then D
# Reattach: screen -r hipaa-ai
# List sessions: screen -ls
```

### Using Tmux:

```bash
# Install tmux (if not installed)
sudo yum install tmux -y  # For RHEL/CentOS
# or
sudo apt-get install tmux -y  # For Ubuntu

# Start a new tmux session
tmux new -s hipaa-ai

# Set environment variables and start service (same as screen)
export OPENAI_API_KEY="your-actual-api-key"
cd ~/hipaa-ai-investigation-system
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Detach: Press Ctrl+B, then D
# Reattach: tmux attach -t hipaa-ai
# List sessions: tmux ls
```

## Option 4: Create a Startup Script

### Create startup script:

```bash
nano ~/start-hipaa-ai.sh
```

Add this content:

```bash
#!/bin/bash

# Set environment variables
export OPENAI_API_KEY="your-actual-api-key"
export SECRET_KEY="dev-secret-key-change-in-production"
export ENCRYPTION_KEY="dev-encryption-key-change-in-production"
export DATABASE_URL="sqlite:///./investigation.db"
export DEBUG=False

# Navigate to project directory
cd ~/hipaa-ai-investigation-system

# Start the service
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Make it executable:

```bash
chmod +x ~/start-hipaa-ai.sh
```

Run it:

```bash
~/start-hipaa-ai.sh
```

## Persistent Environment Variables

### Option A: Add to ~/.bashrc (for user sessions)

```bash
echo 'export OPENAI_API_KEY="your-actual-api-key"' >> ~/.bashrc
echo 'export SECRET_KEY="dev-secret-key-change-in-production"' >> ~/.bashrc
echo 'export ENCRYPTION_KEY="dev-encryption-key-change-in-production"' >> ~/.bashrc
echo 'export DATABASE_URL="sqlite:///./investigation.db"' >> ~/.bashrc
echo 'export DEBUG=False' >> ~/.bashrc

# Reload
source ~/.bashrc
```

### Option B: Create .env file (recommended)

```bash
cd ~/hipaa-ai-investigation-system
nano .env
```

Add:

```
OPENAI_API_KEY=your-actual-api-key
SECRET_KEY=dev-secret-key-change-in-production
ENCRYPTION_KEY=dev-encryption-key-change-in-production
DATABASE_URL=sqlite:///./investigation.db
DEBUG=False
```

The application will automatically load from `.env` file (python-dotenv is already installed).

## Security Group Configuration

Make sure port 8000 is open:

1. AWS Console → EC2 → Security Groups
2. Find your instance's security group
3. Add inbound rule:
   - Type: Custom TCP
   - Port: 8000
   - Source: Your IP or 0.0.0.0/0 (for testing)

## Firewall Configuration (if applicable)

### For firewalld (RHEL/CentOS):

```bash
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### For ufw (Ubuntu):

```bash
sudo ufw allow 8000/tcp
sudo ufw reload
```

## Quick Start (Current Setup)

If you just want to run it now:

```bash
cd ~/hipaa-ai-investigation-system

# Set environment variables
export OPENAI_API_KEY="your-actual-api-key"
export SECRET_KEY="dev-secret-key-change-in-production"
export ENCRYPTION_KEY="dev-encryption-key-change-in-production"
export DATABASE_URL="sqlite:///./investigation.db"
export DEBUG=False

# Start in background
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

# Check it's running
curl http://localhost:8000/health
```

## Recommended: Systemd Service

For production use, **Option 2 (Systemd Service)** is recommended because:
- ✅ Automatically starts on boot
- ✅ Automatically restarts if it crashes
- ✅ Easy to manage (start/stop/restart)
- ✅ Centralized logging
- ✅ Runs as a proper service


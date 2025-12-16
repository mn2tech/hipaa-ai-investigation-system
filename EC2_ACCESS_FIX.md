# Fix EC2 Access from Outside

## Problem
Cannot connect to service on port 8000 from outside the EC2 instance.

## Solution: Configure Security Group

### Step 1: Check Security Group in AWS Console

1. Go to AWS Console → EC2
2. Find your instance (IP: 98.90.130.74)
3. Click on the instance
4. Go to "Security" tab
5. Click on the Security Group name

### Step 2: Add Inbound Rule

1. Click "Edit inbound rules"
2. Click "Add rule"
3. Configure:
   - **Type**: Custom TCP
   - **Port range**: 8000
   - **Source**: 
     - For testing: `0.0.0.0/0` (allows from anywhere)
     - For production: Your specific IP address
4. Click "Save rules"

### Step 3: Verify Service is Running

On your EC2 instance:
```bash
# Check if service is running
curl http://localhost:8000/health

# Check what's listening on port 8000
ss -tulpn | grep 8000
# Or
sudo netstat -tulpn | grep 8000
```

### Step 4: Check Firewall (if applicable)

If you have a firewall running:
```bash
# For firewalld (RHEL/CentOS)
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# For ufw (Ubuntu)
sudo ufw allow 8000/tcp
```

## Alternative: Use SSH Tunnel

If you can't modify security group, use SSH tunnel:

```bash
# From your Windows machine
ssh -L 8000:localhost:8000 raj@98.90.130.74

# Then access via:
# http://localhost:8000
```

## Test After Configuration

```bash
# From your Windows machine
curl http://98.90.130.74:8000/health
```


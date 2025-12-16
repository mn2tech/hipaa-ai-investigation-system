# Quick Deployment Guide - AWS

## 🚀 Recommended: AWS App Runner (Best for FastAPI)

AWS App Runner is perfect for containerized FastAPI applications.

### Quick Start (5 minutes):

1. **Go to AWS App Runner Console**
   - Visit: https://console.aws.amazon.com/apprunner
   - Click "Create service"

2. **Connect Your Repository**
   - Source: "Source code repository"
   - Provider: GitHub
   - Connect and select: `mn2tech/hipaa-ai-investigation-system`
   - Branch: `main`

3. **Configure Build**
   - Build type: **Docker**
   - Dockerfile path: `Dockerfile` (already in repo)
   - Port: `8000`

4. **Configure Service**
   - Service name: `hipaa-ai-investigation`
   - CPU: 1 vCPU
   - Memory: 2 GB
   - Auto-deploy: Enabled

5. **Add Environment Variables**
   ```
   SECRET_KEY=<generate-secure-key>
   ENCRYPTION_KEY=<generate-using-python-command>
   OPENAI_API_KEY=<your-openai-key>
   DATABASE_URL=<your-database-url>
   DEBUG=False
   ```

6. **Create and Deploy**
   - Click "Create & deploy"
   - Wait 5-10 minutes
   - Get your URL: `https://xxxxx.awsapprunner.com`

### Generate Encryption Key:
```bash
python -c "from src.security.encryption import generate_encryption_key; print(generate_encryption_key())"
```

---

## Alternative: AWS Amplify Hosting

If you specifically want to use AWS Amplify, you'll need to:

1. **Use Amplify for Frontend** (if you add one later)
2. **Use App Runner for Backend** (recommended)
3. **Or convert to Serverless Functions** (requires code changes)

### Using Amplify Console:

1. Go to AWS Amplify Console
2. Connect your GitHub repository
3. Build settings: Use `amplify.yml` (already created)
4. Deploy

**Note**: Amplify is better for static sites and serverless functions. For FastAPI, App Runner is the better choice.

---

## 📝 Next Steps After Deployment

1. **Set up Database** (AWS RDS PostgreSQL recommended)
2. **Configure Environment Variables** in App Runner
3. **Set up Custom Domain** (optional)
4. **Configure Monitoring** (CloudWatch)
5. **Set up CI/CD** (automatic deployments on git push)

---

## 🔗 Your Deployment Files

- ✅ `Dockerfile` - Container configuration
- ✅ `amplify.yml` - Amplify build config
- ✅ `.dockerignore` - Docker ignore rules
- ✅ `DEPLOYMENT.md` - Detailed deployment guide

---

**Ready to deploy?** Follow the AWS App Runner steps above!


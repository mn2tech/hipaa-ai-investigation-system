# AWS Amplify Setup for FastAPI

## Important Note

AWS Amplify is primarily designed for frontend applications. For FastAPI backends, there are better options:

1. **AWS App Runner** (Recommended) - Designed for containerized apps
2. **AWS Elastic Beanstalk** - Easy Python deployment
3. **AWS Lambda + API Gateway** - Serverless (requires Mangum)

## Current Setup: Lambda Function Approach

I've configured the app to work with Amplify using Mangum (Lambda adapter), but this has limitations.

### Issues with Amplify for FastAPI:

1. **No persistent server** - Runs as serverless functions
2. **Cold starts** - First request can be slow
3. **Limited runtime** - 15-minute max execution time
4. **Complex routing** - API Gateway integration needed

## Better Alternative: AWS App Runner

### Quick Setup:

1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
2. Create service → Source: GitHub
3. Select repository: `mn2tech/hipaa-ai-investigation-system`
4. Build: Docker (uses Dockerfile)
5. Port: 8000
6. Deploy!

**Why App Runner is better:**
- ✅ Persistent server (no cold starts)
- ✅ Automatic scaling
- ✅ Built-in HTTPS
- ✅ Better for FastAPI
- ✅ Simpler configuration

## If You Must Use Amplify

### Option 1: Amplify + App Runner (Hybrid)

1. Use Amplify for frontend (if you add one)
2. Use App Runner for FastAPI backend
3. Connect via API calls

### Option 2: Convert to Serverless (Current Setup)

The current setup uses Mangum to make FastAPI Lambda-compatible:

1. **Set up Amplify Backend:**
   - Go to Amplify Console
   - Add backend environment
   - Configure Lambda function

2. **Environment Variables:**
   Set in Amplify Console:
   - `SECRET_KEY`
   - `ENCRYPTION_KEY`
   - `OPENAI_API_KEY`
   - `DATABASE_URL`
   - `DEBUG=False`

3. **API Routes:**
   Amplify will create API Gateway routes automatically

### Option 3: Use Amplify Hosting Only

If you just want to host the API docs:
1. Build static docs
2. Host on Amplify
3. Run backend separately (App Runner)

## Recommended Action

**Switch to AWS App Runner** - It's the right tool for FastAPI:

1. Delete current Amplify app (or keep for frontend)
2. Create App Runner service
3. Connect GitHub repo
4. Deploy in 5 minutes

See `DEPLOYMENT.md` for detailed App Runner instructions.


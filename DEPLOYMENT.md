# AWS Amplify Deployment Guide

## Overview

This guide explains how to deploy the HIPAA-Compliant AI Investigation System to AWS Amplify.

## Prerequisites

1. AWS Account
2. AWS Amplify Console access
3. GitHub repository connected (already done: https://github.com/mn2tech/hipaa-ai-investigation-system)

## Deployment Options

### Option 1: AWS Amplify Hosting (Recommended for Full-Stack)

AWS Amplify can host containerized applications. However, for a FastAPI backend, consider these alternatives:

#### Using AWS App Runner (Recommended for FastAPI)

1. **Push Dockerfile to repository** (already created)
2. **Create App Runner service:**
   - Go to AWS App Runner console
   - Create new service
   - Source: GitHub
   - Connect your repository
   - Build: Use Dockerfile
   - Deploy

#### Using AWS Elastic Beanstalk (Easier for Python)

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB:**
   ```bash
   eb init -p python-3.11 hipaa-ai-investigation
   ```

3. **Create environment:**
   ```bash
   eb create hipaa-ai-investigation-env
   ```

4. **Set environment variables:**
   ```bash
   eb setenv SECRET_KEY=your-secret-key \
            ENCRYPTION_KEY=your-encryption-key \
            OPENAI_API_KEY=your-openai-key \
            DATABASE_URL=your-database-url
   ```

### Option 2: AWS Amplify with Lambda Functions

Convert FastAPI endpoints to Lambda functions (requires code refactoring).

### Option 3: AWS Amplify + AWS App Runner (Hybrid)

- Use Amplify for frontend (if you add one)
- Use App Runner for FastAPI backend
- Connect via API Gateway

## Step-by-Step: AWS App Runner Deployment

### 1. Prepare Repository

All files are ready:
- ✅ Dockerfile
- ✅ .dockerignore
- ✅ requirements.txt

### 2. Create App Runner Service

1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
2. Click "Create service"
3. Choose "Source code repository"
4. Connect GitHub and select: `mn2tech/hipaa-ai-investigation-system`
5. Configure:
   - **Build type**: Docker
   - **Dockerfile path**: `Dockerfile`
   - **Port**: `8000`
6. Configure service:
   - **Service name**: `hipaa-ai-investigation`
   - **CPU**: 0.5 vCPU (or 1 vCPU for production)
   - **Memory**: 1 GB (or 2 GB for production)
7. Add environment variables:
   ```
   SECRET_KEY=your-secret-key
   ENCRYPTION_KEY=your-encryption-key
   OPENAI_API_KEY=your-openai-key
   DATABASE_URL=your-database-url
   DEBUG=False
   ```
8. Create service

### 3. Access Your Application

After deployment, App Runner provides a URL like:
```
https://xxxxx.us-east-1.awsapprunner.com
```

### 4. Set Up Custom Domain (Optional)

1. In App Runner service, go to "Custom domains"
2. Add your domain
3. Follow DNS configuration instructions

## Environment Variables Setup

### In AWS App Runner:

1. Go to your service
2. Click "Configuration" → "Environment variables"
3. Add:
   - `SECRET_KEY` - Generate a secure random string
   - `ENCRYPTION_KEY` - Generate using: `python -c "from src.security.encryption import generate_encryption_key; print(generate_encryption_key())"`
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `DATABASE_URL` - Your database connection string
   - `DEBUG=False` - Set to False for production

### Using AWS Secrets Manager (Recommended for Production)

1. Store secrets in AWS Secrets Manager
2. Reference in App Runner environment variables:
   ```
   SECRET_KEY={{ secrets-manager:hipaa-secrets:SECRET_KEY }}
   ```

## Database Setup

### Option 1: AWS RDS (PostgreSQL)

1. Create RDS PostgreSQL instance
2. Set security group to allow App Runner access
3. Update `DATABASE_URL` in environment variables

### Option 2: AWS RDS (SQL Server)

Similar to PostgreSQL setup.

## Security Considerations

1. **HTTPS**: App Runner provides HTTPS by default
2. **Environment Variables**: Use AWS Secrets Manager for sensitive data
3. **VPC**: Configure VPC for database access
4. **IAM Roles**: Use IAM roles for service permissions
5. **WAF**: Consider AWS WAF for additional protection

## Monitoring

1. **CloudWatch Logs**: Automatic log collection
2. **CloudWatch Metrics**: CPU, memory, request metrics
3. **X-Ray**: Enable for distributed tracing (optional)

## Cost Estimation

- **App Runner**: ~$0.007 per vCPU-hour + $0.0008 per GB-hour
- **RDS**: Depends on instance size
- **Data Transfer**: Standard AWS data transfer pricing

## Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Check CloudWatch logs

### Application Won't Start
- Verify environment variables are set
- Check application logs in CloudWatch
- Verify port 8000 is exposed

### Database Connection Issues
- Check security group rules
- Verify DATABASE_URL format
- Check VPC configuration

## Next Steps

1. Set up RDS database
2. Configure environment variables
3. Set up monitoring and alerts
4. Configure custom domain
5. Set up CI/CD pipeline (optional)

## Alternative: AWS Amplify Hosting with Serverless

If you prefer to use Amplify Hosting directly:

1. Convert FastAPI to serverless functions
2. Use Amplify Functions
3. Deploy via Amplify Console

This requires significant code refactoring.

---

**Recommended**: Use AWS App Runner for the FastAPI backend as it's designed for containerized applications and provides automatic scaling and HTTPS.


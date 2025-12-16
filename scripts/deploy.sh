#!/bin/bash
# Deployment script for AWS App Runner

set -e

echo "🚀 Starting deployment process..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t hipaa-ai-investigation:latest .

# Test the image locally (optional)
echo "🧪 Testing Docker image..."
docker run -d -p 8000:8000 --name test-container \
    -e SECRET_KEY=test-secret \
    -e ENCRYPTION_KEY=test-encryption \
    -e DATABASE_URL=sqlite:///./test.db \
    hipaa-ai-investigation:latest

# Wait for container to start
sleep 5

# Test health endpoint
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Health check passed!"
    docker stop test-container
    docker rm test-container
else
    echo "❌ Health check failed!"
    docker stop test-container
    docker rm test-container
    exit 1
fi

echo "✅ Deployment preparation complete!"
echo "📝 Next steps:"
echo "   1. Push code to GitHub"
echo "   2. Create App Runner service in AWS Console"
echo "   3. Connect to GitHub repository"
echo "   4. Configure environment variables"
echo "   5. Deploy!"


"""
AWS Lambda handler for FastAPI application using Mangum.
This allows the FastAPI app to run as a serverless function in AWS Amplify.
"""
from mangum import Mangum
from src.api.main import app

# Create the handler for AWS Lambda
handler = Mangum(app, lifespan="off")

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


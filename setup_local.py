"""
Setup script for local development.
Generates encryption key and creates .env file.
"""
import os
from src.security.encryption import generate_encryption_key

def setup_local_env():
    """Set up local development environment."""
    print("Setting up local development environment...")
    
    # Generate encryption key
    encryption_key = generate_encryption_key()
    
    # Create .env file
    env_content = f"""# Local Development Configuration
# WARNING: These are development values. Change all secrets in production!

# Application Settings
DEBUG=True
APP_NAME="HIPAA-Compliant AI Investigation System"
APP_VERSION="1.0.0"

# Security - CHANGE THESE IN PRODUCTION
SECRET_KEY=dev-secret-key-change-in-production-{os.urandom(16).hex()}
ENCRYPTION_KEY={encryption_key}

# Database (SQLite for local development)
DATABASE_URL=sqlite:///./investigation.db

# OpenAI API (required for AI analysis)
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# File Storage
UPLOAD_DIR=./uploads

# Compliance Settings
AUDIT_LOG_RETENTION_DAYS=2555
ND_RECORD_RETENTION_DAYS=2555
CFR2_COMPLIANCE_ENABLED=True
ND_OPEN_RECORDS_COMPLIANCE=True
"""
    
    env_file = ".env"
    if os.path.exists(env_file):
        response = input(f"{env_file} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n[OK] Created {env_file} file")
    print("\n[!] IMPORTANT: Edit .env and add your OPENAI_API_KEY")
    print("   Get your API key from: https://platform.openai.com/api-keys")
    print("\nNext steps:")
    print("   1. Edit .env and add your OPENAI_API_KEY")
    print("   2. Install dependencies: pip install -r requirements.txt")
    print("   3. Run the server: uvicorn src.api.main:app --reload")
    print("   4. Open browser to: http://localhost:8000/docs")

if __name__ == "__main__":
    setup_local_env()


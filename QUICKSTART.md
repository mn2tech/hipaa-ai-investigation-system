# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9+ installed
- ✅ PostgreSQL database (or SQLite for development)
- ✅ OpenAI API key
- ✅ Git (for cloning)

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Encryption Key
```bash
python -c "from src.security.encryption import generate_encryption_key; print('ENCRYPTION_KEY=' + generate_encryption_key())"
```

### Step 3: Create .env File
Create a `.env` file in the project root with:
```env
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=<key-from-step-2>
DATABASE_URL=sqlite:///./investigation.db
OPENAI_API_KEY=your-openai-api-key
DEBUG=True
```

### Step 4: Run the Application
```bash
uvicorn src.api.main:app --reload
```

### Step 5: Test the API
Open your browser to:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## First Complaint Analysis

1. **Create a Complaint** (via API or Swagger UI at `/docs`):
```bash
curl -X POST "http://localhost:8000/api/complaints" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "complaint_number": "COMP-2024-001",
    "received_date": "2024-01-15T10:00:00Z",
    "licensee_name": "Dr. John Doe",
    "licensee_license_number": "ND-12345",
    "complaint_description": "Test complaint for evaluation"
  }'
```

2. **Run AI Analysis**:
```bash
curl -X POST "http://localhost:8000/api/complaints/{complaint_id}/analyze" \
  -H "Authorization: Bearer <token>"
```

3. **Generate Report**:
```bash
curl -X POST "http://localhost:8000/api/complaints/{complaint_id}/reports" \
  -H "Authorization: Bearer <token>"
```

## Common Issues

### Issue: "OpenAI API key not found"
**Solution**: Ensure `OPENAI_API_KEY` is set in your `.env` file

### Issue: "Encryption key error"
**Solution**: Generate a new encryption key using the command in Step 2

### Issue: "Database connection error"
**Solution**: Check your `DATABASE_URL` in `.env` file

### Issue: Import errors
**Solution**: Ensure you're in the project root and virtual environment is activated

## Next Steps

- Read [API Documentation](docs/API.md) for detailed endpoint information
- Review [Compliance Documentation](docs/COMPLIANCE.md) for compliance requirements
- Check [Architecture Documentation](docs/ARCHITECTURE.md) for system design

## Production Deployment

⚠️ **Important**: Before deploying to production:

1. Change all default secrets and keys
2. Use a production-grade database (PostgreSQL)
3. Configure proper HTTPS/TLS
4. Set up proper authentication (JWT with secure tokens)
5. Configure file storage with encryption
6. Set up monitoring and logging
7. Review and configure all compliance settings
8. Conduct security assessment

See [README.md](README.md) for more detailed setup instructions.


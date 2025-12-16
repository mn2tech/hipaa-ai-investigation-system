# Quick Start Guide - Run Locally

## ✅ Dependencies Installed
All Python dependencies have been installed successfully!

## 🚀 To Run the Server

### Option 1: Using the run script
```bash
python run_local.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Using Python module
```bash
python -m uvicorn src.api.main:app --reload
```

## 📝 Environment Setup

The system will work with default settings, but for full functionality:

1. **Create a `.env` file** in the project root with:
```env
SECRET_KEY=dev-secret-key-change-in-production
ENCRYPTION_KEY=<generate-using-command-below>
DATABASE_URL=sqlite:///./investigation.db
OPENAI_API_KEY=your-openai-api-key-here
DEBUG=True
```

2. **Generate encryption key** (optional, defaults provided):
```bash
python -c "from src.security.encryption import generate_encryption_key; print(generate_encryption_key())"
```

3. **Get OpenAI API key** (required for AI analysis):
   - Visit: https://platform.openai.com/api-keys
   - Add your key to `.env` file

## 🌐 Access the API

Once the server is running:

- **API Root**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Authentication

For local testing, the API uses a placeholder authentication system. All endpoints require a Bearer token, but any token will work in development mode.

Example:
```bash
curl -X GET "http://localhost:8000/health" -H "Authorization: Bearer test-token"
```

## ⚠️ Important Notes

1. **OpenAI API Key**: The AI analysis features require a valid OpenAI API key. Without it, those endpoints will return an error.

2. **Database**: Currently using SQLite for local development. Data is stored in `investigation.db` in the project root.

3. **File Uploads**: Upload directory is set to `./uploads` (will be created automatically).

4. **Security**: The default settings are for **development only**. Change all secrets before production deployment.

## 🧪 Test the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. View API Documentation
Open in browser: http://localhost:8000/docs

### 3. Create a Complaint (requires auth token)
```bash
curl -X POST "http://localhost:8000/api/complaints" \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "complaint_number": "COMP-2024-001",
    "received_date": "2024-01-15T10:00:00Z",
    "licensee_name": "Dr. John Doe",
    "licensee_license_number": "ND-12345",
    "complaint_description": "Test complaint"
  }'
```

## 🐛 Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check for Python version (requires 3.9+)

### Import errors
- Make sure you're in the project root directory
- Verify all dependencies are installed

### OpenAI API errors
- Check that OPENAI_API_KEY is set in `.env` file
- Verify the API key is valid and has credits

### Authentication errors
- In development, any Bearer token works
- Make sure to include `Authorization: Bearer <token>` header

## 📚 Next Steps

1. Explore the API documentation at http://localhost:8000/docs
2. Read [README.md](README.md) for full documentation
3. Check [docs/API.md](docs/API.md) for detailed API information
4. Review [docs/COMPLIANCE.md](docs/COMPLIANCE.md) for compliance details

## 🎉 You're Ready!

The server should now be running. Open http://localhost:8000/docs in your browser to explore the interactive API documentation!


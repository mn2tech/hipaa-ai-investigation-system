# HIPAA-Compliant AI Investigation System

A secure, HIPAA-compliant artificial intelligence solution designed to aid in the investigation of complaints against licensees. This system streamlines the investigatory process by analyzing complaint and response documentation, recommending information-gathering strategies, and generating comprehensive summary reports for STATE Investigatory Panel members.

## Compliance & Security

This system is designed to maintain strict compliance with:
- **HIPAA** (Health Insurance Portability and Accountability Act)
- **42 CFR Part 2** (Confidentiality of Substance Use Disorder Patient Records)
- **North Dakota Century Code** provisions:
  - N.D.C.C. § 43-17-32.1(5)
  - N.D.C.C. § 43-17-41
  - N.D.C.C. § 43-17.1-08
  - N.D.C.C. § 43-17.3-07
  - N.D.C.C. § 43-17.4 (Article VIII)
  - N.D.C.C. § 44-04-18.32 (Open Records Law)

## Features

- **Document Analysis**: AI-powered analysis of complaint and response documentation
- **Strategy Recommendations**: Intelligent recommendations for information-gathering strategies
- **Report Generation**: Comprehensive summary reports for Investigatory Panel members
- **Secure Data Handling**: End-to-end encryption and access controls for sensitive information
- **Audit Logging**: Complete audit trails for compliance and security monitoring

## Project Structure

```
├── src/
│   ├── core/              # Core system components
│   ├── ai/                # AI analysis engine
│   ├── security/          # Security and compliance modules
│   ├── reports/           # Report generation system
│   └── api/               # API endpoints
├── config/                # Configuration files
├── tests/                 # Test suite
├── docs/                  # Documentation
└── requirements.txt       # Python dependencies
```

## Installation

### Prerequisites
- Python 3.9 or higher
- PostgreSQL (or compatible database)
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "AI Paul"
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `SECRET_KEY`: Secret key for JWT tokens
- `ENCRYPTION_KEY`: Encryption key for data at rest (generate using `python -c "from src.security.encryption import generate_encryption_key; print(generate_encryption_key())"`)
- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: OpenAI API key

5. Initialize database (when database models are implemented):
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

6. Run the application:
```bash
python -m src.api.main
# Or using uvicorn directly:
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

## Usage

### API Endpoints

See [API Documentation](docs/API.md) for detailed endpoint documentation.

### Basic Workflow

1. **Create a Complaint**: POST `/api/complaints`
2. **Upload Documents**: POST `/api/complaints/{complaint_id}/documents`
3. **Run AI Analysis**: POST `/api/complaints/{complaint_id}/analyze`
4. **Generate Report**: POST `/api/complaints/{complaint_id}/reports`
5. **Export Report**: GET `/api/complaints/{complaint_id}/reports/{report_id}/export?format=text`

### Example: Creating and Analyzing a Complaint

```python
import requests

# Create complaint
complaint_data = {
    "complaint_number": "COMP-2024-001",
    "received_date": "2024-01-15T10:00:00Z",
    "licensee_name": "Dr. John Doe",
    "licensee_license_number": "ND-12345",
    "complaint_description": "Alleged violation of professional standards"
}

response = requests.post(
    "http://localhost:8000/api/complaints",
    json=complaint_data,
    headers={"Authorization": "Bearer <token>"}
)
complaint = response.json()

# Run analysis
analysis_response = requests.post(
    f"http://localhost:8000/api/complaints/{complaint['id']}/analyze",
    headers={"Authorization": "Bearer <token>"}
)
analysis = analysis_response.json()
```

## Security Considerations

- All PHI (Protected Health Information) is encrypted at rest and in transit
- Access controls enforce role-based permissions
- Comprehensive audit logging for all system activities
- Regular security assessments and compliance reviews

## License

[License information]


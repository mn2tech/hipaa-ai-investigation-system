# System Architecture

## Overview

The HIPAA-Compliant AI Investigation System is designed as a modular, secure platform for investigating complaints against licensees. The system uses AI to analyze complaints and responses, recommend investigation strategies, and generate comprehensive reports.

## Architecture Components

### 1. Core Layer (`src/core/`)
- **Models**: Data models for complaints, documents, analyses, and reports
- **Business Logic**: Core business rules and workflows

### 2. Security Layer (`src/security/`)
- **Encryption**: Data encryption at rest and in transit
- **Access Control**: Role-based access control (RBAC)
- **Audit Logging**: Comprehensive audit trails
- **Compliance**: HIPAA, 42 CFR Part 2, and ND state law compliance checking

### 3. AI Layer (`src/ai/`)
- **Analyzer**: AI-powered analysis of complaints and responses
- **Strategy Recommendations**: Information-gathering strategy suggestions
- **Risk Assessment**: Automated risk evaluation

### 4. Reports Layer (`src/reports/`)
- **Generator**: Comprehensive report generation for Panel members
- **Export**: Multiple export formats (text, JSON, PDF)

### 5. API Layer (`src/api/`)
- **REST API**: FastAPI-based RESTful API
- **Authentication**: JWT-based authentication
- **Endpoints**: Complaint, document, analysis, and report endpoints

## Data Flow

1. **Complaint Creation**: User creates complaint via API
2. **Document Upload**: Documents uploaded and encrypted
3. **AI Analysis**: System analyzes complaint and documents
4. **Strategy Recommendations**: AI suggests investigation strategies
5. **Report Generation**: Comprehensive report generated for Panel
6. **Audit Logging**: All actions logged for compliance

## Security Architecture

### Encryption
- Symmetric encryption (Fernet) for data at rest
- TLS/HTTPS for data in transit
- Key management via environment variables

### Access Control
- Role-based permissions
- Security classification-based access
- Per-resource authorization

### Audit Logging
- All system activities logged
- PHI and CFR2 access specially tracked
- 7-year retention period

## Compliance Architecture

### HIPAA
- Encryption of PHI
- Access controls
- Audit logging
- Business Associate Agreements (for third parties)

### 42 CFR Part 2
- Enhanced protection for substance use disorder records
- Written consent requirements
- Enhanced audit logging
- Redisclosure restrictions

### North Dakota State Law
- Record retention requirements
- Open records law compliance
- Required field validation
- Statute-specific compliance checks

## Technology Stack

- **Language**: Python 3.9+
- **Framework**: FastAPI
- **AI/ML**: OpenAI GPT-4, LangChain
- **Database**: PostgreSQL (recommended)
- **Encryption**: Cryptography (Fernet)
- **Logging**: Structlog

## Deployment Considerations

1. **Environment Variables**: All sensitive configuration via environment variables
2. **Database**: Use encrypted database connections
3. **File Storage**: Encrypted file storage for documents
4. **API Security**: HTTPS only, rate limiting, input validation
5. **Monitoring**: Comprehensive logging and monitoring
6. **Backup**: Regular encrypted backups
7. **Disaster Recovery**: Documented recovery procedures

## Scalability

- Stateless API design for horizontal scaling
- Database connection pooling
- Caching for frequently accessed data
- Async processing for AI analysis
- Queue system for background tasks (future enhancement)


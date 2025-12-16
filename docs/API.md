# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All API endpoints require authentication using Bearer tokens in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Health Check
```
GET /health
```
Returns system health status.

### Create Complaint
```
POST /api/complaints
```
Creates a new complaint.

**Request Body:**
```json
{
  "complaint_number": "COMP-2024-001",
  "received_date": "2024-01-15T10:00:00Z",
  "licensee_name": "Dr. John Doe",
  "licensee_license_number": "ND-12345",
  "complaint_description": "Alleged violation of professional standards",
  "status": "received"
}
```

**Response:** Complaint object

### Get Complaint
```
GET /api/complaints/{complaint_id}
```
Retrieves a complaint by ID.

**Response:** Complaint object

### Analyze Complaint
```
POST /api/complaints/{complaint_id}/analyze
```
Runs AI analysis on a complaint and its documents.

**Response:** AIAnalysis object with:
- Key findings
- Recommended strategies
- Risk assessment
- Compliance notes
- Confidence score

### Generate Report
```
POST /api/complaints/{complaint_id}/reports
```
Generates a comprehensive investigation report for Panel members.

**Response:** InvestigationReport object

### Export Report
```
GET /api/complaints/{complaint_id}/reports/{report_id}/export?format={format}
```
Exports a report in the specified format (text, json, pdf).

**Query Parameters:**
- `format`: Export format (text, json, pdf)

### Upload Document
```
POST /api/complaints/{complaint_id}/documents
```
Uploads a document for a complaint.

**Form Data:**
- `file`: File to upload
- `document_type`: Type of document (complaint, response, evidence, etc.)

**Response:** Document object

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Rate Limiting

API rate limiting may be implemented. Check response headers for rate limit information.


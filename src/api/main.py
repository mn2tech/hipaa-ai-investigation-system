"""
FastAPI application for the HIPAA-compliant AI Investigation System.
"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import structlog

from src.core.models import (
    Complaint,
    Document,
    AIAnalysis,
    InvestigationReport,
    ComplaintStatus
)
from src.ai.analyzer import ComplaintAnalyzer
from src.reports.generator import ReportGenerator
from src.security.audit import audit_logger
from src.security.access_control import Role, Permission, AccessControl
from config.settings import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="HIPAA-compliant AI Investigation System for STATE"
)

# CORS middleware (configure appropriately for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services (lazy initialization to handle missing API key)
_analyzer = None
report_generator = ReportGenerator()

def get_analyzer():
    """Get or create the analyzer instance."""
    global _analyzer
    if _analyzer is None:
        try:
            _analyzer = ComplaintAnalyzer()
        except (ValueError, Exception) as e:
            # API key not set or other error, analyzer will be None
            logger.warning("Analyzer not available", error=str(e))
            pass
    return _analyzer


# Dependency for authentication (placeholder - implement proper auth)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user. Placeholder implementation."""
    # In production, validate JWT token and return user object
    # For now, return a mock user
    return {
        "user_id": "user123",
        "role": Role.INVESTIGATOR,
        "email": "investigator@state.gov"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/complaints", response_model=Complaint)
async def create_complaint(
    complaint: Complaint,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new complaint.
    Requires: CREATE_COMPLAINT permission
    """
    # Check permissions
    if not AccessControl.has_permission(current_user["role"], Permission.CREATE_COMPLAINT):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Log action
    audit_logger.log_action(
        user_id=current_user["user_id"],
        action="create_complaint",
        resource_type="complaint",
        resource_id=complaint.complaint_number,
        details={"complaint_data": complaint.model_dump()}
    )
    
    # In production, save to database
    complaint.id = f"comp_{datetime.utcnow().timestamp()}"
    complaint.created_at = datetime.utcnow()
    complaint.updated_at = datetime.utcnow()
    
    logger.info("Complaint created", complaint_id=complaint.id, user_id=current_user["user_id"])
    return complaint


@app.get("/api/complaints/{complaint_id}", response_model=Complaint)
async def get_complaint(
    complaint_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a complaint by ID.
    Requires: VIEW_COMPLAINT permission
    """
    if not AccessControl.has_permission(current_user["role"], Permission.VIEW_COMPLAINT):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Log data access
    audit_logger.log_data_access(
        user_id=current_user["user_id"],
        resource_type="complaint",
        resource_id=complaint_id,
        classification="confidential"
    )
    
    # In production, fetch from database
    # For now, return mock data
    raise HTTPException(status_code=404, detail="Complaint not found")


@app.post("/api/complaints/{complaint_id}/analyze", response_model=AIAnalysis)
async def analyze_complaint(
    complaint_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Run AI analysis on a complaint.
    Requires: RUN_ANALYSIS permission
    """
    if not AccessControl.has_permission(current_user["role"], Permission.RUN_ANALYSIS):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Log action
    audit_logger.log_action(
        user_id=current_user["user_id"],
        action="run_analysis",
        resource_type="complaint",
        resource_id=complaint_id
    )
    
    # In production, fetch complaint and documents from database
    # For now, create mock data
    complaint = Complaint(
        id=complaint_id,
        complaint_number="COMP-2024-001",
        received_date=datetime.utcnow(),
        licensee_name="Dr. John Doe",
        licensee_license_number="ND-12345",
        complaint_description="Sample complaint description"
    )
    
    complaint_docs = []
    response_docs = []
    
    # Run analysis
    analyzer_instance = get_analyzer()
    if analyzer_instance is None:
        raise HTTPException(
            status_code=503,
            detail="AI analysis service unavailable. Please configure OPENAI_API_KEY in environment variables."
        )
    
    try:
        analysis = analyzer_instance.analyze_complaint(complaint, complaint_docs, response_docs)
        logger.info("Analysis completed", complaint_id=complaint_id)
        return analysis
    except Exception as e:
        logger.error("Analysis failed", complaint_id=complaint_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/complaints/{complaint_id}/reports", response_model=InvestigationReport)
async def generate_report(
    complaint_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate a comprehensive investigation report.
    Requires: GENERATE_REPORT permission
    """
    if not AccessControl.has_permission(current_user["role"], Permission.GENERATE_REPORT):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Log action
    audit_logger.log_action(
        user_id=current_user["user_id"],
        action="generate_report",
        resource_type="complaint",
        resource_id=complaint_id
    )
    
    # In production, fetch data from database
    # For now, create mock data
    complaint = Complaint(
        id=complaint_id,
        complaint_number="COMP-2024-001",
        received_date=datetime.utcnow(),
        licensee_name="Dr. John Doe",
        licensee_license_number="ND-12345",
        complaint_description="Sample complaint description"
    )
    
    documents = []
    ai_analysis = AIAnalysis(
        complaint_id=complaint_id,
        key_findings=["Sample finding"],
        recommended_strategies=["Sample strategy"],
        risk_assessment={"level": "medium"},
        compliance_notes=["Sample note"],
        confidence_score=0.8,
        model_version=settings.OPENAI_MODEL
    )
    
    # Generate report
    try:
        report = report_generator.generate_panel_report(
            complaint, documents, ai_analysis, current_user["user_id"]
        )
        logger.info("Report generated", complaint_id=complaint_id)
        return report
    except Exception as e:
        logger.error("Report generation failed", complaint_id=complaint_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@app.get("/api/complaints/{complaint_id}/reports/{report_id}/export")
async def export_report(
    complaint_id: str,
    report_id: str,
    format: str = "text",
    current_user: dict = Depends(get_current_user)
):
    """
    Export a report in various formats.
    Requires: EXPORT_REPORT permission
    """
    if not AccessControl.has_permission(current_user["role"], Permission.EXPORT_REPORT):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Log action
    audit_logger.log_action(
        user_id=current_user["user_id"],
        action="export_report",
        resource_type="report",
        resource_id=report_id,
        details={"format": format}
    )
    
    # In production, fetch report from database
    # For now, return mock
    raise HTTPException(status_code=404, detail="Report not found")


@app.post("/api/complaints/{complaint_id}/documents")
async def upload_document(
    complaint_id: str,
    file: UploadFile = File(...),
    document_type: str = "other",
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a document for a complaint.
    Requires: UPLOAD_DOCUMENT permission
    """
    if not AccessControl.has_permission(current_user["role"], Permission.UPLOAD_DOCUMENT):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Log action
    audit_logger.log_action(
        user_id=current_user["user_id"],
        action="upload_document",
        resource_type="document",
        resource_id=file.filename or "unknown",
        details={"complaint_id": complaint_id, "document_type": document_type}
    )
    
    # In production, save file with encryption
    # For now, return mock
    document = Document(
        complaint_id=complaint_id,
        document_type=document_type,
        filename=file.filename or "unknown",
        file_path=f"/uploads/{file.filename}",
        file_size=0,
        mime_type=file.content_type or "application/octet-stream",
        uploaded_by=current_user["user_id"],
        security_classification="confidential",
        encrypted=True
    )
    
    logger.info("Document uploaded", complaint_id=complaint_id, filename=file.filename)
    return document


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


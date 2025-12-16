"""
Data models for the investigation system.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ComplaintStatus(str, Enum):
    """Status of a complaint investigation."""
    RECEIVED = "received"
    UNDER_REVIEW = "under_review"
    INVESTIGATION_IN_PROGRESS = "investigation_in_progress"
    AWAITING_RESPONSE = "awaiting_response"
    ANALYSIS_COMPLETE = "analysis_complete"
    REPORT_GENERATED = "report_generated"
    CLOSED = "closed"


class DocumentType(str, Enum):
    """Types of documents in the system."""
    COMPLAINT = "complaint"
    RESPONSE = "response"
    EVIDENCE = "evidence"
    CORRESPONDENCE = "correspondence"
    REPORT = "report"
    OTHER = "other"


class SecurityClassification(str, Enum):
    """Security classification levels."""
    PUBLIC = "public"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PHI = "phi"  # Protected Health Information
    CFR2 = "cfr2"  # 42 CFR Part 2 protected


class Complaint(BaseModel):
    """Complaint model."""
    id: Optional[str] = None
    complaint_number: str = Field(..., description="Unique complaint identifier")
    received_date: datetime
    complainant_name: Optional[str] = None
    licensee_name: str
    licensee_license_number: str
    complaint_description: str
    status: ComplaintStatus = ComplaintStatus.RECEIVED
    assigned_investigator: Optional[str] = None
    security_classification: SecurityClassification = SecurityClassification.CONFIDENTIAL
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "complaint_number": "COMP-2024-001",
                "received_date": "2024-01-15T10:00:00Z",
                "licensee_name": "Dr. John Doe",
                "licensee_license_number": "ND-12345",
                "complaint_description": "Alleged violation of professional standards",
                "status": "received"
            }
        }


class Document(BaseModel):
    """Document model for storing complaint-related documents."""
    id: Optional[str] = None
    complaint_id: str
    document_type: DocumentType
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    uploaded_by: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    security_classification: SecurityClassification
    encrypted: bool = True
    checksum: Optional[str] = None  # For integrity verification


class AIAnalysis(BaseModel):
    """AI analysis results for a complaint."""
    id: Optional[str] = None
    complaint_id: str
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    key_findings: List[str]
    recommended_strategies: List[str]
    risk_assessment: Dict[str, Any]
    compliance_notes: List[str]
    confidence_score: float = Field(ge=0.0, le=1.0)
    model_version: str


class InvestigationReport(BaseModel):
    """Comprehensive investigation report for Panel members."""
    id: Optional[str] = None
    complaint_id: str
    report_date: datetime = Field(default_factory=datetime.utcnow)
    executive_summary: str
    complaint_details: Dict[str, Any]
    response_analysis: Dict[str, Any]
    key_findings: List[str]
    recommended_strategies: List[str]
    compliance_considerations: List[str]
    risk_assessment: Dict[str, Any]
    generated_by: str
    version: int = 1


class AuditLog(BaseModel):
    """Audit log entry for compliance tracking."""
    id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Dict[str, Any] = {}
    success: bool = True


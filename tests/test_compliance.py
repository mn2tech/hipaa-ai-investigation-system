"""
Tests for compliance checking functionality.
"""
import pytest
from datetime import datetime
from src.core.models import Complaint, Document, SecurityClassification, ComplaintStatus
from src.security.compliance import ComplianceChecker


def test_hipaa_compliance_check():
    """Test HIPAA compliance checking."""
    complaint = Complaint(
        complaint_number="COMP-001",
        received_date=datetime.utcnow(),
        licensee_name="Dr. Test",
        licensee_license_number="ND-123",
        complaint_description="Test complaint"
    )
    
    # Test with encrypted PHI documents
    phi_doc = Document(
        complaint_id="comp1",
        document_type="complaint",
        filename="phi_doc.pdf",
        file_path="/path/to/doc",
        file_size=1000,
        mime_type="application/pdf",
        uploaded_by="user1",
        security_classification=SecurityClassification.PHI,
        encrypted=True
    )
    
    result = ComplianceChecker.check_hipaa_compliance(complaint, [phi_doc])
    assert "compliant" in result
    assert isinstance(result["compliant"], bool)


def test_cfr2_compliance_check():
    """Test 42 CFR Part 2 compliance checking."""
    complaint = Complaint(
        complaint_number="COMP-001",
        received_date=datetime.utcnow(),
        licensee_name="Dr. Test",
        licensee_license_number="ND-123",
        complaint_description="Test complaint"
    )
    
    result = ComplianceChecker.check_cfr2_compliance(complaint, [])
    assert "compliant" in result


def test_nd_state_law_compliance():
    """Test North Dakota state law compliance checking."""
    complaint = Complaint(
        complaint_number="COMP-001",
        received_date=datetime.utcnow(),
        licensee_name="Dr. Test",
        licensee_license_number="ND-123",
        complaint_description="Test complaint"
    )
    
    result = ComplianceChecker.check_nd_state_law_compliance(complaint)
    assert "compliant" in result


"""
Compliance checking and validation for HIPAA, 42 CFR Part 2, and ND state laws.
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
from src.core.models import Complaint, Document, SecurityClassification
from config.settings import settings


class ComplianceChecker:
    """Service for checking compliance with various regulations."""
    
    @staticmethod
    def check_hipaa_compliance(complaint: Complaint, documents: List[Document]) -> Dict[str, Any]:
        """
        Check HIPAA compliance for a complaint and its documents.
        
        Args:
            complaint: Complaint to check
            documents: List of documents associated with complaint
            
        Returns:
            Dictionary with compliance status and issues
        """
        issues = []
        warnings = []
        
        # Check if PHI is properly classified
        phi_docs = [d for d in documents if d.security_classification == SecurityClassification.PHI]
        if phi_docs:
            unencrypted_phi = [d for d in phi_docs if not d.encrypted]
            if unencrypted_phi:
                issues.append("PHI documents must be encrypted")
        
        # Check audit logging (would check if access to PHI is logged)
        # This would be checked against audit logs in production
        
        # Check access controls
        # This would verify that only authorized users can access PHI
        
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "checked_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def check_cfr2_compliance(complaint: Complaint, documents: List[Document]) -> Dict[str, Any]:
        """
        Check 42 CFR Part 2 compliance.
        
        42 CFR Part 2 requires:
        - Written consent for disclosure
        - Special handling of substance use disorder records
        - Enhanced audit logging
        
        Args:
            complaint: Complaint to check
            documents: List of documents associated with complaint
            
        Returns:
            Dictionary with compliance status and issues
        """
        issues = []
        warnings = []
        
        # Check for CFR2 classified documents
        cfr2_docs = [d for d in documents if d.security_classification == SecurityClassification.CFR2]
        
        if cfr2_docs:
            # CFR2 documents require special handling
            unencrypted_cfr2 = [d for d in cfr2_docs if not d.encrypted]
            if unencrypted_cfr2:
                issues.append("42 CFR Part 2 documents must be encrypted")
            
            # Check if consent documentation exists (would check in production)
            warnings.append("Verify written consent for 42 CFR Part 2 disclosures")
        
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "checked_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def check_nd_state_law_compliance(complaint: Complaint) -> Dict[str, Any]:
        """
        Check compliance with North Dakota state laws.
        
        Relevant statutes:
        - N.D.C.C. § 43-17-32.1(5)
        - N.D.C.C. § 43-17-41
        - N.D.C.C. § 43-17.1-08
        - N.D.C.C. § 43-17.3-07
        - N.D.C.C. § 43-17.4 (Article VIII)
        - N.D.C.C. § 44-04-18.32 (Open Records Law)
        
        Args:
            complaint: Complaint to check
            
        Returns:
            Dictionary with compliance status and issues
        """
        issues = []
        warnings = []
        
        # Check record retention requirements
        # ND state law may require specific retention periods
        retention_days = settings.ND_RECORD_RETENTION_DAYS
        if retention_days < 2555:  # 7 years minimum
            warnings.append(f"Record retention set to {retention_days} days, verify compliance with ND law")
        
        # Check open records law compliance
        # N.D.C.C. § 44-04-18.32 may require certain records to be available
        # This would need to be checked against specific requirements
        
        # Verify complaint has required fields per ND statutes
        required_fields = [
            "complaint_number",
            "licensee_name",
            "licensee_license_number",
            "complaint_description"
        ]
        
        for field in required_fields:
            if not getattr(complaint, field, None):
                issues.append(f"Missing required field: {field}")
        
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "checked_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def comprehensive_compliance_check(
        complaint: Complaint,
        documents: List[Document]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive compliance check for all applicable regulations.
        
        Args:
            complaint: Complaint to check
            documents: List of documents associated with complaint
            
        Returns:
            Dictionary with comprehensive compliance status
        """
        hipaa = ComplianceChecker.check_hipaa_compliance(complaint, documents)
        cfr2 = ComplianceChecker.check_cfr2_compliance(complaint, documents)
        nd_law = ComplianceChecker.check_nd_state_law_compliance(complaint)
        
        all_compliant = (
            hipaa["compliant"] and
            cfr2["compliant"] and
            nd_law["compliant"]
        )
        
        all_issues = hipaa["issues"] + cfr2["issues"] + nd_law["issues"]
        all_warnings = hipaa["warnings"] + cfr2["warnings"] + nd_law["warnings"]
        
        return {
            "overall_compliant": all_compliant,
            "hipaa": hipaa,
            "cfr2": cfr2,
            "nd_state_law": nd_law,
            "all_issues": all_issues,
            "all_warnings": all_warnings,
            "checked_at": datetime.utcnow().isoformat()
        }


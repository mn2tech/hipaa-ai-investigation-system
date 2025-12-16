"""
Report generation system for creating comprehensive summary reports
for STATE Investigatory Panel members.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.core.models import (
    Complaint,
    Document,
    AIAnalysis,
    InvestigationReport,
    ComplaintStatus
)
from src.security.compliance import ComplianceChecker
import structlog

logger = structlog.get_logger(__name__)


class ReportGenerator:
    """Service for generating comprehensive investigation reports."""
    
    def __init__(self):
        self.compliance_checker = ComplianceChecker()
    
    def generate_panel_report(
        self,
        complaint: Complaint,
        documents: List[Document],
        ai_analysis: AIAnalysis,
        generated_by: str
    ) -> InvestigationReport:
        """
        Generate a comprehensive report for Investigatory Panel members.
        
        Args:
            complaint: The complaint being investigated
            documents: All documents associated with the complaint
            ai_analysis: AI analysis results
            generated_by: User ID of person generating the report
            
        Returns:
            InvestigationReport object
        """
        logger.info("Generating panel report", complaint_id=complaint.id)
        
        # Perform compliance check
        compliance_status = self.compliance_checker.comprehensive_compliance_check(
            complaint, documents
        )
        
        # Organize documents by type
        complaint_docs = [d for d in documents if d.document_type == "complaint"]
        response_docs = [d for d in documents if d.document_type == "response"]
        evidence_docs = [d for d in documents if d.document_type == "evidence"]
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            complaint, ai_analysis, compliance_status
        )
        
        # Prepare complaint details
        complaint_details = self._prepare_complaint_details(complaint, complaint_docs)
        
        # Prepare response analysis
        response_analysis = self._prepare_response_analysis(response_docs, ai_analysis)
        
        # Prepare compliance considerations
        compliance_considerations = self._prepare_compliance_considerations(
            compliance_status
        )
        
        # Create report
        report = InvestigationReport(
            complaint_id=complaint.id or "",
            report_date=datetime.utcnow(),
            executive_summary=executive_summary,
            complaint_details=complaint_details,
            response_analysis=response_analysis,
            key_findings=ai_analysis.key_findings,
            recommended_strategies=ai_analysis.recommended_strategies,
            compliance_considerations=compliance_considerations,
            risk_assessment=ai_analysis.risk_assessment,
            generated_by=generated_by,
            version=1
        )
        
        logger.info("Panel report generated", complaint_id=complaint.id)
        return report
    
    def _generate_executive_summary(
        self,
        complaint: Complaint,
        ai_analysis: AIAnalysis,
        compliance_status: Dict[str, Any]
    ) -> str:
        """Generate executive summary for the report."""
        summary_parts = [
            f"Investigation Report: {complaint.complaint_number}",
            f"Licensee: {complaint.licensee_name} (License: {complaint.licensee_license_number})",
            f"Status: {complaint.status.value}",
            "",
            "EXECUTIVE SUMMARY",
            f"This report summarizes the investigation of complaint {complaint.complaint_number} "
            f"received on {complaint.received_date.strftime('%Y-%m-%d')}.",
            "",
            "KEY FINDINGS:",
        ]
        
        for i, finding in enumerate(ai_analysis.key_findings[:5], 1):  # Top 5 findings
            summary_parts.append(f"{i}. {finding}")
        
        summary_parts.extend([
            "",
            f"RISK ASSESSMENT: {ai_analysis.risk_assessment.get('level', 'unknown').upper()}",
            f"  Urgency: {ai_analysis.risk_assessment.get('urgency', 'unknown')}",
            "",
            f"COMPLIANCE STATUS: {'COMPLIANT' if compliance_status['overall_compliant'] else 'ISSUES IDENTIFIED'}",
        ])
        
        return "\n".join(summary_parts)
    
    def _prepare_complaint_details(
        self,
        complaint: Complaint,
        complaint_docs: List[Document]
    ) -> Dict[str, Any]:
        """Prepare detailed complaint information."""
        return {
            "complaint_number": complaint.complaint_number,
            "received_date": complaint.received_date.isoformat(),
            "complainant": complaint.complainant_name or "Not disclosed",
            "licensee_name": complaint.licensee_name,
            "licensee_license_number": complaint.licensee_license_number,
            "description": complaint.complaint_description,
            "status": complaint.status.value,
            "assigned_investigator": complaint.assigned_investigator or "Not assigned",
            "security_classification": complaint.security_classification.value,
            "associated_documents": len(complaint_docs),
            "document_list": [
                {
                    "filename": doc.filename,
                    "type": doc.document_type.value,
                    "uploaded": doc.uploaded_at.isoformat()
                }
                for doc in complaint_docs
            ]
        }
    
    def _prepare_response_analysis(
        self,
        response_docs: List[Document],
        ai_analysis: AIAnalysis
    ) -> Dict[str, Any]:
        """Prepare analysis of licensee responses."""
        return {
            "response_documents_count": len(response_docs),
            "response_documents": [
                {
                    "filename": doc.filename,
                    "uploaded": doc.uploaded_at.isoformat(),
                    "security_classification": doc.security_classification.value
                }
                for doc in response_docs
            ],
            "ai_analysis_summary": {
                "key_findings": ai_analysis.key_findings,
                "confidence_score": ai_analysis.confidence_score,
                "model_version": ai_analysis.model_version
            }
        }
    
    def _prepare_compliance_considerations(
        self,
        compliance_status: Dict[str, Any]
    ) -> List[str]:
        """Prepare compliance considerations for the report."""
        considerations = []
        
        # HIPAA considerations
        if not compliance_status["hipaa"]["compliant"]:
            considerations.append(
                "HIPAA COMPLIANCE ISSUES: " + "; ".join(compliance_status["hipaa"]["issues"])
            )
        else:
            considerations.append("HIPAA: Compliant")
        
        # 42 CFR Part 2 considerations
        if not compliance_status["cfr2"]["compliant"]:
            considerations.append(
                "42 CFR PART 2 COMPLIANCE ISSUES: " + "; ".join(compliance_status["cfr2"]["issues"])
            )
        elif compliance_status["cfr2"]["warnings"]:
            considerations.append(
                "42 CFR PART 2 WARNINGS: " + "; ".join(compliance_status["cfr2"]["warnings"])
            )
        else:
            considerations.append("42 CFR Part 2: Compliant")
        
        # ND State Law considerations
        if not compliance_status["nd_state_law"]["compliant"]:
            considerations.append(
                "ND STATE LAW COMPLIANCE ISSUES: " + "; ".join(compliance_status["nd_state_law"]["issues"])
            )
        else:
            considerations.append("ND State Law: Compliant")
        
        # Add any general warnings
        if compliance_status["all_warnings"]:
            considerations.append("GENERAL WARNINGS: " + "; ".join(compliance_status["all_warnings"]))
        
        return considerations
    
    def export_report_to_text(self, report: InvestigationReport) -> str:
        """
        Export report to plain text format.
        
        Args:
            report: The investigation report
            
        Returns:
            Plain text representation of the report
        """
        lines = [
            "=" * 80,
            "INVESTIGATION REPORT",
            "=" * 80,
            f"Report Date: {report.report_date.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Complaint ID: {report.complaint_id}",
            f"Generated By: {report.generated_by}",
            f"Version: {report.version}",
            "",
            report.executive_summary,
            "",
            "=" * 80,
            "COMPLAINT DETAILS",
            "=" * 80,
        ]
        
        # Add complaint details
        for key, value in report.complaint_details.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: {value}")
        
        lines.extend([
            "",
            "=" * 80,
            "RESPONSE ANALYSIS",
            "=" * 80,
        ])
        
        # Add response analysis
        for key, value in report.response_analysis.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            elif isinstance(value, dict):
                lines.append(f"{key}:")
                for sub_key, sub_value in value.items():
                    lines.append(f"  {sub_key}: {sub_value}")
            else:
                lines.append(f"{key}: {value}")
        
        lines.extend([
            "",
            "=" * 80,
            "KEY FINDINGS",
            "=" * 80,
        ])
        
        for i, finding in enumerate(report.key_findings, 1):
            lines.append(f"{i}. {finding}")
        
        lines.extend([
            "",
            "=" * 80,
            "RECOMMENDED STRATEGIES",
            "=" * 80,
        ])
        
        for i, strategy in enumerate(report.recommended_strategies, 1):
            lines.append(f"{i}. {strategy}")
        
        lines.extend([
            "",
            "=" * 80,
            "COMPLIANCE CONSIDERATIONS",
            "=" * 80,
        ])
        
        for consideration in report.compliance_considerations:
            lines.append(f"- {consideration}")
        
        lines.extend([
            "",
            "=" * 80,
            "RISK ASSESSMENT",
            "=" * 80,
        ])
        
        for key, value in report.risk_assessment.items():
            lines.append(f"{key}: {value}")
        
        lines.append("")
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def export_report_to_json(self, report: InvestigationReport) -> str:
        """
        Export report to JSON format.
        
        Args:
            report: The investigation report
            
        Returns:
            JSON representation of the report
        """
        import json
        from datetime import datetime
        
        # Convert datetime objects to ISO strings for JSON serialization
        report_dict = report.model_dump()
        report_dict["report_date"] = report.report_date.isoformat()
        
        return json.dumps(report_dict, indent=2, default=str)


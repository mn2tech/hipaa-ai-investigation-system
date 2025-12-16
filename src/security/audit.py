"""
Audit logging system for HIPAA compliance.
Maintains comprehensive audit trails of all system activities.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from src.core.models import AuditLog
import structlog
from config.settings import settings


logger = structlog.get_logger(__name__)


class AuditLogger:
    """Audit logging service for compliance tracking."""
    
    def __init__(self):
        self.logger = structlog.get_logger(
            "audit",
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer()
            ]
        )
    
    def log_action(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True
    ) -> AuditLog:
        """
        Log an audit event.
        
        Args:
            user_id: ID of user performing action
            action: Action being performed (e.g., "view_complaint", "download_document")
            resource_type: Type of resource (e.g., "complaint", "document")
            resource_id: ID of the resource
            ip_address: IP address of user
            user_agent: User agent string
            details: Additional details about the action
            success: Whether the action was successful
            
        Returns:
            AuditLog entry
        """
        audit_entry = AuditLog(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details or {},
            success=success
        )
        
        # Log to structured logger
        self.logger.info(
            "audit_event",
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            success=success
        )
        
        # In production, this would also write to a database
        # db_session.add(audit_entry)
        # db_session.commit()
        
        return audit_entry
    
    def log_data_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        classification: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log access to sensitive data (required for HIPAA and 42 CFR Part 2).
        
        Args:
            user_id: ID of user accessing data
            resource_type: Type of resource being accessed
            resource_id: ID of the resource
            classification: Security classification of the data
            ip_address: IP address of user
            user_agent: User agent string
        """
        self.log_action(
            user_id=user_id,
            action="data_access",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details={"classification": classification},
            success=True
        )
    
    def log_phi_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log access to PHI (Protected Health Information).
        
        Args:
            user_id: ID of user accessing PHI
            resource_type: Type of resource containing PHI
            resource_id: ID of the resource
            ip_address: IP address of user
            user_agent: User agent string
        """
        self.log_action(
            user_id=user_id,
            action="phi_access",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details={"phi_accessed": True},
            success=True
        )
    
    def log_cfr2_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log access to 42 CFR Part 2 protected information.
        
        Args:
            user_id: ID of user accessing CFR2 data
            resource_type: Type of resource containing CFR2 data
            resource_id: ID of the resource
            ip_address: IP address of user
            user_agent: User agent string
        """
        self.log_action(
            user_id=user_id,
            action="cfr2_access",
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details={"cfr2_accessed": True},
            success=True
        )


# Global audit logger instance
audit_logger = AuditLogger()


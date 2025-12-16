"""
Access control and authorization system.
Implements role-based access control (RBAC) for HIPAA compliance.
"""
from typing import List, Optional, Set
from enum import Enum
from functools import wraps
from src.core.models import SecurityClassification


class Role(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    INVESTIGATOR = "investigator"
    PANEL_MEMBER = "panel_member"
    REVIEWER = "reviewer"
    AUDITOR = "auditor"
    READ_ONLY = "read_only"


class Permission(str, Enum):
    """System permissions."""
    # Complaint permissions
    CREATE_COMPLAINT = "create_complaint"
    VIEW_COMPLAINT = "view_complaint"
    EDIT_COMPLAINT = "edit_complaint"
    DELETE_COMPLAINT = "delete_complaint"
    
    # Document permissions
    UPLOAD_DOCUMENT = "upload_document"
    VIEW_DOCUMENT = "view_document"
    DOWNLOAD_DOCUMENT = "download_document"
    DELETE_DOCUMENT = "delete_document"
    
    # AI Analysis permissions
    RUN_ANALYSIS = "run_analysis"
    VIEW_ANALYSIS = "view_analysis"
    
    # Report permissions
    GENERATE_REPORT = "generate_report"
    VIEW_REPORT = "view_report"
    EXPORT_REPORT = "export_report"
    
    # Audit permissions
    VIEW_AUDIT_LOG = "view_audit_log"
    EXPORT_AUDIT_LOG = "export_audit_log"
    
    # Administrative permissions
    MANAGE_USERS = "manage_users"
    MANAGE_SETTINGS = "manage_settings"


# Role-Permission mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: set(Permission),  # Admins have all permissions
    Role.INVESTIGATOR: {
        Permission.CREATE_COMPLAINT,
        Permission.VIEW_COMPLAINT,
        Permission.EDIT_COMPLAINT,
        Permission.UPLOAD_DOCUMENT,
        Permission.VIEW_DOCUMENT,
        Permission.DOWNLOAD_DOCUMENT,
        Permission.RUN_ANALYSIS,
        Permission.VIEW_ANALYSIS,
        Permission.GENERATE_REPORT,
        Permission.VIEW_REPORT,
        Permission.EXPORT_REPORT,
    },
    Role.PANEL_MEMBER: {
        Permission.VIEW_COMPLAINT,
        Permission.VIEW_DOCUMENT,
        Permission.VIEW_ANALYSIS,
        Permission.VIEW_REPORT,
        Permission.EXPORT_REPORT,
    },
    Role.REVIEWER: {
        Permission.VIEW_COMPLAINT,
        Permission.VIEW_DOCUMENT,
        Permission.VIEW_ANALYSIS,
        Permission.VIEW_REPORT,
    },
    Role.AUDITOR: {
        Permission.VIEW_AUDIT_LOG,
        Permission.EXPORT_AUDIT_LOG,
        Permission.VIEW_COMPLAINT,  # Read-only access
    },
    Role.READ_ONLY: {
        Permission.VIEW_COMPLAINT,
        Permission.VIEW_DOCUMENT,
        Permission.VIEW_ANALYSIS,
        Permission.VIEW_REPORT,
    },
}


class AccessControl:
    """Access control service."""
    
    @staticmethod
    def has_permission(role: Role, permission: Permission) -> bool:
        """
        Check if a role has a specific permission.
        
        Args:
            role: User role
            permission: Permission to check
            
        Returns:
            True if role has permission, False otherwise
        """
        role_perms = ROLE_PERMISSIONS.get(role, set())
        return permission in role_perms
    
    @staticmethod
    def can_access_classification(role: Role, classification: SecurityClassification) -> bool:
        """
        Check if a role can access data with a specific security classification.
        
        Args:
            role: User role
            classification: Security classification level
            
        Returns:
            True if role can access, False otherwise
        """
        # PHI and CFR2 data require special access
        if classification in [SecurityClassification.PHI, SecurityClassification.CFR2]:
            return role in [Role.ADMIN, Role.INVESTIGATOR, Role.PANEL_MEMBER]
        
        # Restricted data requires investigator or above
        if classification == SecurityClassification.RESTRICTED:
            return role in [Role.ADMIN, Role.INVESTIGATOR, Role.PANEL_MEMBER, Role.REVIEWER]
        
        # Confidential and public accessible to all authenticated users
        return True
    
    @staticmethod
    def get_accessible_classifications(role: Role) -> List[SecurityClassification]:
        """
        Get list of security classifications accessible to a role.
        
        Args:
            role: User role
            
        Returns:
            List of accessible security classifications
        """
        all_classifications = list(SecurityClassification)
        return [
            cls for cls in all_classifications
            if AccessControl.can_access_classification(role, cls)
        ]


def require_permission(permission: Permission):
    """
    Decorator to require a specific permission for a function.
    
    Args:
        permission: Required permission
        
    Usage:
        @require_permission(Permission.VIEW_COMPLAINT)
        def view_complaint(complaint_id: str):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, this would check the current user's role
            # For now, this is a placeholder that would be integrated with authentication
            # user_role = get_current_user_role()
            # if not AccessControl.has_permission(user_role, permission):
            #     raise PermissionError(f"User does not have {permission} permission")
            return func(*args, **kwargs)
        return wrapper
    return decorator


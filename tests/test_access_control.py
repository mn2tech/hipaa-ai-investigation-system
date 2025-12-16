"""
Tests for access control functionality.
"""
import pytest
from src.security.access_control import AccessControl, Role, Permission, SecurityClassification


def test_permission_checking():
    """Test permission checking for roles."""
    # Admin should have all permissions
    assert AccessControl.has_permission(Role.ADMIN, Permission.CREATE_COMPLAINT)
    assert AccessControl.has_permission(Role.ADMIN, Permission.VIEW_AUDIT_LOG)
    
    # Investigator should have investigation permissions
    assert AccessControl.has_permission(Role.INVESTIGATOR, Permission.CREATE_COMPLAINT)
    assert AccessControl.has_permission(Role.INVESTIGATOR, Permission.RUN_ANALYSIS)
    assert not AccessControl.has_permission(Role.INVESTIGATOR, Permission.MANAGE_USERS)
    
    # Read-only should have limited permissions
    assert AccessControl.has_permission(Role.READ_ONLY, Permission.VIEW_COMPLAINT)
    assert not AccessControl.has_permission(Role.READ_ONLY, Permission.CREATE_COMPLAINT)


def test_classification_access():
    """Test security classification access control."""
    # Admin can access all classifications
    assert AccessControl.can_access_classification(Role.ADMIN, SecurityClassification.PHI)
    
    # Investigator can access PHI
    assert AccessControl.can_access_classification(Role.INVESTIGATOR, SecurityClassification.PHI)
    
    # Read-only cannot access PHI
    assert not AccessControl.can_access_classification(Role.READ_ONLY, SecurityClassification.PHI)


"""
Tests for encryption functionality.
"""
import pytest
from src.security.encryption import EncryptionService, generate_encryption_key


def test_encryption_decryption():
    """Test basic encryption and decryption."""
    key = generate_encryption_key()
    service = EncryptionService(key=key)
    
    original_text = "This is sensitive PHI data"
    encrypted = service.encrypt(original_text)
    decrypted = service.decrypt(encrypted)
    
    assert decrypted == original_text
    assert encrypted != original_text


def test_encryption_key_generation():
    """Test encryption key generation."""
    key = generate_encryption_key()
    assert isinstance(key, str)
    assert len(key) > 0


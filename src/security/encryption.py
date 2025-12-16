"""
Encryption utilities for securing PHI and sensitive data.
Implements encryption at rest and in transit as required by HIPAA.
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from typing import Optional
from config.settings import settings


class EncryptionService:
    """Service for encrypting and decrypting sensitive data."""
    
    def __init__(self, key: Optional[str] = None):
        """
        Initialize encryption service.
        
        Args:
            key: Encryption key. If not provided, uses key from settings.
        """
        if key is None:
            key = settings.ENCRYPTION_KEY
        
        # Ensure key is in correct format for Fernet
        if isinstance(key, str):
            # If key is base64 string, use directly
            try:
                base64.b64decode(key)
                self.cipher = Fernet(key.encode() if isinstance(key, str) else key)
            except Exception:
                # Generate key from password using PBKDF2
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'hipaa_compliant_salt',  # In production, use unique salt per record
                    iterations=100000,
                    backend=default_backend()
                )
                key_bytes = kdf.derive(key.encode())
                self.cipher = Fernet(base64.urlsafe_b64encode(key_bytes))
        else:
            self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data.
        
        Args:
            data: Plain text data to encrypt
            
        Returns:
            Encrypted data as base64 string
        """
        if not data:
            return data
        
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Encrypted data as base64 string
            
        Returns:
            Decrypted plain text data
        """
        if not encrypted_data:
            return encrypted_data
        
        decoded = base64.b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(decoded)
        return decrypted.decode()
    
    def encrypt_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        Encrypt a file.
        
        Args:
            file_path: Path to file to encrypt
            output_path: Optional output path. If not provided, adds .enc extension
            
        Returns:
            Path to encrypted file
        """
        if output_path is None:
            output_path = file_path + ".enc"
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted = self.cipher.encrypt(data)
        
        with open(output_path, 'wb') as f:
            f.write(encrypted)
        
        return output_path
    
    def decrypt_file(self, encrypted_file_path: str, output_path: Optional[str] = None) -> str:
        """
        Decrypt a file.
        
        Args:
            encrypted_file_path: Path to encrypted file
            output_path: Optional output path. If not provided, removes .enc extension
            
        Returns:
            Path to decrypted file
        """
        if output_path is None:
            output_path = encrypted_file_path.replace(".enc", "")
        
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted = self.cipher.decrypt(encrypted_data)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        
        return output_path


def generate_encryption_key() -> str:
    """
    Generate a new encryption key for use with Fernet.
    
    Returns:
        Base64-encoded encryption key
    """
    return Fernet.generate_key().decode()


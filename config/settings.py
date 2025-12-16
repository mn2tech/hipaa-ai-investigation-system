"""
Configuration settings for the HIPAA-compliant AI Investigation System.
All sensitive settings should be loaded from environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "HIPAA-Compliant AI Investigation System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Encryption
    ENCRYPTION_KEY: str = "dev-encryption-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "sqlite:///./investigation.db"
    
    # AI/LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.3  # Lower temperature for more consistent, factual outputs
    
    # HIPAA Compliance
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years as per HIPAA requirements
    ENCRYPTION_AT_REST: bool = True
    ENCRYPTION_IN_TRANSIT: bool = True
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 50
    
    # 42 CFR Part 2 Compliance
    CFR2_COMPLIANCE_ENABLED: bool = True
    CFR2_AUDIT_LOGGING: bool = True
    
    # North Dakota State Law Compliance
    ND_OPEN_RECORDS_COMPLIANCE: bool = True
    ND_RECORD_RETENTION_DAYS: int = 2555


# Global settings instance
settings = Settings()


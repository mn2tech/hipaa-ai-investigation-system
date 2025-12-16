"""
Configuration settings for the HIPAA-compliant AI Investigation System.
All sensitive settings should be loaded from environment variables.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "HIPAA-Compliant AI Investigation System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Security
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Encryption
    ENCRYPTION_KEY: str = Field(default="dev-encryption-key-change-in-production", env="ENCRYPTION_KEY")
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./investigation.db", env="DATABASE_URL")
    
    # AI/LLM Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.3  # Lower temperature for more consistent, factual outputs
    
    # HIPAA Compliance
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years as per HIPAA requirements
    ENCRYPTION_AT_REST: bool = True
    ENCRYPTION_IN_TRANSIT: bool = True
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE_MB: int = 50
    
    # 42 CFR Part 2 Compliance
    CFR2_COMPLIANCE_ENABLED: bool = True
    CFR2_AUDIT_LOGGING: bool = True
    
    # North Dakota State Law Compliance
    ND_OPEN_RECORDS_COMPLIANCE: bool = True
    ND_RECORD_RETENTION_DAYS: int = 2555
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


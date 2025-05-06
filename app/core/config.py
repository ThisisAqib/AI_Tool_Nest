"""
Application Configuration Module

This module handles all configuration settings for the application,
loading them from environment variables and providing type-safe access
through Pydantic settings management.
"""

from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List, Optional
import json
from pydantic import validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are loaded from environment variables and validated
    using Pydantic. Default values are provided where appropriate.
    """

    # Base application settings
    PROJECT_NAME: str = "AI Tool Nest"
    VERSION: str = "0.1.0"

    # Security settings
    SECRET_KEY: str

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str]

    # FastAPI Settings
    HOST: str
    PORT: int
    RELOAD: bool

    # Text Summarizer API Settings
    AI_TOOL_NEST_API_URL: str
    AI_TOOL_NEST_API_KEY: str

    class Config:
        """Pydantic settings configuration."""

        case_sensitive = True
        env_file = ".env"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            """
            Custom environment variable parser.

            Handles special cases like parsing JSON strings for CORS origins.

            Args:
                field_name (str): Name of the environment variable
                raw_val (str): Raw value from environment

            Returns:
                Parsed value appropriate for the field
            """
            if field_name == "BACKEND_CORS_ORIGINS":
                return json.loads(raw_val)
            return raw_val


# Create global settings instance
settings = Settings()

# Define project paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = ROOT_DIR / "app" / "static"
TEMPLATE_DIR = ROOT_DIR / "app" / "templates"

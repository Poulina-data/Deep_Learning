"""
Configuration module for Boston House Price Prediction application.
Loads environment variables and defines application-wide settings.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Base directory (project root)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration class."""

    # ----- Flask -----
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "change-me-in-production")
    DEBUG: bool = False
    TESTING: bool = False

    # ----- Request limits -----
    MAX_CONTENT_LENGTH: int = 1 * 1024 * 1024  # 1 MB

    # ----- Model paths -----
    MODEL_PATH: Path = BASE_DIR / "model" / "boston_house_model.h5"
    SCALER_PATH: Path = BASE_DIR / "model" / "scaler.pkl"

    # ----- Logging -----
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "CHANGE_THIS_IN_PRODUCTION")


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True


# ---------------------------------------------------------------------------
# Configuration selector
# ---------------------------------------------------------------------------
_CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

ACTIVE_ENV = os.environ.get("FLASK_ENV", "development")
ActiveConfig = _CONFIG_MAP.get(ACTIVE_ENV, DevelopmentConfig)

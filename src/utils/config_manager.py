# src/utils/config_manager.py
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Determine the project root based on this file's location
# This assumes config_manager.py is in src/utils/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(PROJECT_ROOT, 'config', '.env')

# Load .env file from the config directory
try:
    # Ensure the path exists before trying to load
    if os.path.exists(ENV_PATH):
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        logger.info(f"Loaded environment variables from: {ENV_PATH}")
    else:
        logger.warning(f".env file not found at: {ENV_PATH}. Relying on system environment variables.")
except Exception as e:
    logger.error(f"Error loading .env file from {ENV_PATH}: {e}")


def get_config(key: str, default: str = None) -> str | None:
    """Retrieves a configuration value from environment variables."""
    return os.getenv(key, default)

# Example Usage:
# OPENAI_API_KEY = get_config("OPENAI_API_KEY")
# PDF_SOURCE_DIR = get_config("PDF_SOURCE_DIR", "./data/raw")

# print(f"Project Root: {PROJECT_ROOT}")
# print(f"Env Path: {ENV_PATH}")
# print(f"Test Env Var: {get_config('TEST_VAR', 'DefaultValue')}")
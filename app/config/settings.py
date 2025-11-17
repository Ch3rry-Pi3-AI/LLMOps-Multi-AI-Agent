"""
settings.py
===========

Configuration module for the **LLMOps Multi-AI Agent** project.

This module loads environmental variables from a `.env` file and provides a
simple `Settings` class that centralises access to API keys and configuration
constants used across the application.

The design keeps configuration logic clean, explicit, and easily testable.  
It also avoids hard-coding secrets directly in the codebase.
"""

# ======================================================================
# Imports
# ======================================================================

# Load environment variables from a .env file
from dotenv import load_dotenv
import os

# Immediately load variables into the environment
load_dotenv()


# ======================================================================
# Settings Class
# ======================================================================

class Settings:
    """
    Container for application-wide configuration values.

    This class retrieves API keys and fixed configuration settings used
    throughout the Multi-AI Agent system. All values are resolved at import
    time, ensuring consistent access from any part of the project.

    Attributes
    ----------
    GROQ_API_KEY : str or None
        API key for the Groq language model service, loaded from `.env`.

    TAVILY_API_KEY : str or None
        API key for Tavily search integration, also loaded from `.env`.

    ALLOWED_MODEL_NAMES : list of str
        A list of permitted LLM model identifiers that may be used by
        the agent. Restricting valid models promotes safety, reproducibility,
        and easier debugging.
    """

    # --------------------------------------------------------------
    # Environment variables
    # --------------------------------------------------------------

    # Retrieve Groq API key from environment (None if missing)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Retrieve Tavily API key from environment
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    # --------------------------------------------------------------
    # Allowed model configuration
    # --------------------------------------------------------------

    # Define the list of safe model names available to the system
    ALLOWED_MODEL_NAMES = [
        "llama3-70b-8192",
        "llama-3.3-70b-versatile"
    ]


# ======================================================================
# Instantiate global settings object
# ======================================================================

# Create a single reusable settings instance for the application
settings = Settings()

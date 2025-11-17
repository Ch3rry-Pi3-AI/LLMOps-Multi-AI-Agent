"""
main.py
=======

Entry point for the **LLMOps Multi-AI Agent** application.

This module launches both the FastAPI backend (Uvicorn) and the Streamlit
frontend UI. The backend is responsible for agent execution, while the
frontend provides an interactive interface for user queries.

The backend runs inside a separate thread to allow both services to operate
concurrently from a single command. Logging and structured exception handling
ensure that failures are captured clearly during start-up.
"""

# ======================================================================
# Imports
# ======================================================================

# Run external processes such as Uvicorn or Streamlit
import subprocess

# Used to run the backend in a separate thread
import threading

# Simple time delay to ensure backend starts before frontend
import time

# Load environment variables from .env
from dotenv import load_dotenv

# Project-wide logging utility
from app.common.logger import get_logger

# Structured custom exception class
from app.common.custom_exception import CustomException


# ======================================================================
# Initialisation
# ======================================================================

# Create a module-level logger
logger = get_logger(__name__)

# Load environment variables into the runtime
load_dotenv()


# ======================================================================
# Backend Launcher
# ======================================================================

def run_backend():
    """
    Start the FastAPI backend service using Uvicorn.

    Raises
    ------
    CustomException
        If the backend fails to start or an unexpected error occurs.
    """
    try:
        # Log backend start-up
        logger.info("Starting backend service...")

        # Launch Uvicorn to serve the FastAPI application
        subprocess.run(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"],
            check=True
        )

    except Exception as e:
        logger.error("Problem with backend service")
        raise CustomException("Failed to start backend", error_detail=e)


# ======================================================================
# Frontend Launcher
# ======================================================================

def run_frontend():
    """
    Start the Streamlit frontend UI.

    Raises
    ------
    CustomException
        If the frontend fails to launch or an unexpected error occurs.
    """
    try:
        # Log frontend start-up
        logger.info("Starting frontend service...")

        # Launch Streamlit to serve the UI
        subprocess.run(
            ["streamlit", "run", "app/frontend/ui.py"],
            check=True
        )

    except Exception as e:
        logger.error("Problem with frontend service")
        raise CustomException("Failed to start frontend", error_detail=e)


# ======================================================================
# Main Entry Point
# ======================================================================

if __name__ == "__main__":
    try:
        # Start backend in a separate thread so frontend can launch concurrently
        threading.Thread(target=run_backend).start()

        # Give the backend time to initialise
        time.sleep(2)

        # Start the Streamlit UI
        run_frontend()

    except CustomException as e:
        # Log full exception details in case of failure
        logger.exception(f"CustomException occurred: {str(e)}")

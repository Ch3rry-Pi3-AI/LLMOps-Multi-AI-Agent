# ======================================================================
# Base Image
# ======================================================================
# Use a lightweight Python 3.10 image as the parent environment.
# "slim" provides a minimal OS footprint while still supporting
# required Python libraries and build tooling when needed.
FROM python:3.12-slim


# ======================================================================
# Environment Variables
# ======================================================================
# PYTHONDONTWRITEBYTECODE:
#   Prevents Python from writing .pyc files to the filesystem,
#   keeping the container clean.
#
# PYTHONUNBUFFERED:
#   Ensures output is sent straight to the console without buffering,
#   which is essential for real-time logs in Docker environments.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# ======================================================================
# Working Directory
# ======================================================================
# Set the working directory inside the container.
# All subsequent commands will operate relative to /app.
WORKDIR /app


# ======================================================================
# System Dependencies
# ======================================================================
# Install system-level build tools and curl. These are often needed
# for some Python packages that rely on C extensions.
# After installation, clean up apt cache to minimise image size.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


# ======================================================================
# Application Source Code
# ======================================================================
# Copy the entire project directory from the host into /app inside
# the container. This includes the app folder, config, frontend,
# backend, and setup.py.
COPY . .


# ======================================================================
# Python Dependencies
# ======================================================================
# Install Python packages defined in setup.py in editable mode (-e).
# Using --no-cache-dir avoids caching wheels, reducing final image size.
RUN pip install --no-cache-dir -e .


# ======================================================================
# Exposed Ports
# ======================================================================
# 8501 → Streamlit frontend UI
# 9999 → FastAPI backend API
EXPOSE 8501
EXPOSE 9999


# ======================================================================
# Application Entry Point
# ======================================================================
# Start the full Multi-AI Agent application.
# This launches both backend (Uvicorn) and frontend (Streamlit)
# through the unified runner defined in app/main.py.
CMD ["python", "app/main.py"]

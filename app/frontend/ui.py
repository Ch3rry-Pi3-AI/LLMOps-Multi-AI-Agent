"""
ui.py
=====

Streamlit-based frontend interface for the **LLMOps Multi-AI Agent** project.

This module provides a simple web UI that allows users to:

* Select a Groq model
* Define a system prompt
* Enable or disable Tavily-powered web search
* Enter a user query
* Send the request to the FastAPI backend
* Display the final AI response returned by the agent

It acts as the visual interaction layer between the user and the Multi-AI
Agent’s reasoning engine.
"""

# ======================================================================
# Imports
# ======================================================================

# Streamlit UI framework
import streamlit as st

# HTTP client for communicating with the FastAPI backend
import requests

# Project configuration (list of allowed model names, environment variables)
from app.config.settings import settings

# Project-wide logging utility
from app.common.logger import get_logger

# Custom exception class for structured error reporting
from app.common.custom_exception import CustomException


# ======================================================================
# Initialisation
# ======================================================================

# Create a logger specific to this module
logger = get_logger(__name__)

# Configure global Streamlit page settings
st.set_page_config(page_title="Multi AI Agent", layout="centered")

# Display main page title
st.title("Multi AI Agent using Groq and Tavily")


# ======================================================================
# User Input Controls
# ======================================================================

# Text area for defining the agent's system-level instruction
system_prompt = st.text_area("Define your AI Agent:", height=70)

# Dropdown to select one of the allowed Groq models
selected_model = st.selectbox("Select your AI model:", settings.ALLOWED_MODEL_NAMES)

# Checkbox to enable/disable Tavily-powered web search
allow_web_search = st.checkbox("Allow web search")

# Text area where the user enters their query
user_query = st.text_area("Enter your query:", height=150)


# ======================================================================
# Backend API Configuration
# ======================================================================

# URL of the backend FastAPI `/chat` endpoint
API_URL = "http://127.0.0.1:9999/chat"


# ======================================================================
# Submit Button Logic
# ======================================================================

# When the "Ask Agent" button is clicked and the query is not empty
if st.button("Ask Agent") and user_query.strip():

    # Prepare payload for backend API
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search,
    }

    try:
        # Log outgoing request to backend
        logger.info("Sending request to backend")

        # Make POST request to backend API
        response = requests.post(API_URL, json=payload)

        # --------------------------------------------------------------
        # Successful Response
        # --------------------------------------------------------------
        if response.status_code == 200:

            # Extract agent's generated response
            agent_response = response.json().get("response", "")

            logger.info("Successfully received response from backend")

            # Display the agent's final answer
            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

        # --------------------------------------------------------------
        # Backend Returned Error
        # --------------------------------------------------------------
        else:
            logger.error("Backend error encountered")
            st.error("Error communicating with backend")

    # --------------------------------------------------------------
    # Network/Unexpected Error
    # --------------------------------------------------------------
    except Exception as e:
        logger.error("Error occurred while sending request to backend")
        st.error(str(CustomException("Failed to communicate to backend", error_detail=e)))

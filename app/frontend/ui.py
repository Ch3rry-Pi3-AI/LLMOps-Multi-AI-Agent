"""
ui.py
=====

Streamlit-based frontend interface for the **LLMOps Multi-AI Agent** project.

This module provides a role-based, interactive UI that allows users to:

* Select a persona preset (e.g. Medical Information, Legal Information, Analyst)
* Choose a Groq model from allowed configurations
* Enable or disable Tavily-powered web search
* Define or customise a system prompt
* Enter their query
* Send the request to the FastAPI backend
* Display the final AI-generated response

The interface acts as the visual entry point to the Multi-AI Agent’s reasoning
engine, offering a streamlined way to test different modes of instruction and
model behaviour through a clean, simple layout.
"""

# ======================================================================
# Imports
# ======================================================================

# Streamlit UI framework
import streamlit as st

# HTTP client for communicating with the FastAPI backend
import requests

# Project configuration (allowed models, environment settings)
from app.config.settings import settings

# Project-wide logging utility
from app.common.logger import get_logger

# Custom exception class for structured error reporting
from app.common.custom_exception import CustomException


# ======================================================================
# Initialisation
# ======================================================================

# Logger for this module
logger = get_logger(__name__)

# Configure the Streamlit page layout
st.set_page_config(page_title="Multi AI Agent", layout="wide")


# ======================================================================
# Role Presets
# ======================================================================

# Predefined system prompts for various agent personas
ROLE_PRESETS = {
    "General Assistant": (
        "You are a helpful, neutral AI assistant. "
        "Answer clearly, concisely, and avoid speculation."
    ),
    "Medical Information (non-diagnostic)": (
        "You are an AI that provides general, non-diagnostic medical information. "
        "You are NOT a doctor and you do NOT give medical advice. "
        "Always encourage users to consult a qualified healthcare professional "
        "for diagnosis, treatment, or urgent concerns."
    ),
    "Legal Information (non-advisory)": (
        "You are an AI that provides general legal information, not legal advice. "
        "You are NOT a lawyer. Encourage users to consult a qualified legal "
        "professional for advice specific to their situation."
    ),
    "Journalist / Analyst": (
        "You are an analytical journalist. You explain issues clearly, lay out "
        "multiple perspectives, avoid taking sides, and distinguish facts from opinion."
    ),
    "Technical Expert": (
        "You are a highly skilled technical expert. Provide precise, step-by-step "
        "explanations, include caveats where appropriate, and avoid hand-waving."
    ),
}

# Backend API endpoint
API_URL = "http://127.0.0.1:9999/chat"


# ======================================================================
# Layout: Sidebar (Configuration) and Main Panel (Chat Interface)
# ======================================================================

# Page title
st.title("Multi AI Agent")

# Sidebar contains all configuration options
with st.sidebar:
    st.header("⚙️ Agent Configuration")

    # Dropdown for role preset
    selected_role = st.selectbox(
        "Select agent role:",
        list(ROLE_PRESETS.keys()),
        index=0,
    )

    # Dropdown for Groq model selection
    selected_model = st.selectbox(
        "Select your AI model:",
        settings.ALLOWED_MODEL_NAMES,
    )

    # Toggle for enabling Tavily-based web search
    allow_web_search = st.checkbox("Allow web search", value=False)

    st.markdown("---")
    st.caption("You may edit the system prompt manually in the main panel.")


# ======================================================================
# Main Panel Inputs: system prompt, query, and action button
# ======================================================================

# Retrieve default role-based prompt and allow user edits
default_prompt = ROLE_PRESETS.get(selected_role, ROLE_PRESETS["General Assistant"])
system_prompt = st.text_area(
    "System prompt (agent instructions):",
    value=default_prompt,
    height=120,
)

# User's natural language query
user_query = st.text_area("Enter your query:", height=160)

# Split layout for button spacing
col1, col2 = st.columns([1, 3])

with col1:
    ask_button = st.button("Ask Agent")

with col2:
    st.write("")  # simple layout spacer


# ======================================================================
# Backend Communication Logic
# ======================================================================

# When the button is pressed and query is not empty
if ask_button and user_query.strip():

    # Construct payload for backend API call
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search,
    }

    try:
        logger.info("Sending request to backend")

        # Show loading indicator while waiting on backend
        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json=payload)

        # --------------------------------------------------------------
        # Backend returned success
        # --------------------------------------------------------------
        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

        # --------------------------------------------------------------
        # Backend returned an error status
        # --------------------------------------------------------------
        else:
            logger.error(f"Backend error. Status code: {response.status_code}")
            st.error("Error communicating with backend. Please check the logs.")

    except Exception as e:
        # Network-level or unexpected exceptions
        logger.error("Error occurred while sending request to backend")
        st.error(str(CustomException("Failed to communicate to backend", error_detail=e)))

# Handle case where button was pressed with no query entered
elif ask_button and not user_query.strip():
    st.warning("Please enter a query before asking the agent.")

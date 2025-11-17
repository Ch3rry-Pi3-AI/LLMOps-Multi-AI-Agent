"""
ui.py
=====

Streamlit-based frontend interface for the **LLMOps Multi-AI Agent** project.

Provides:
* Role presets (e.g. medical / legal / journalist style)
* Model selection
* Optional web search
* Query input and response display
"""

import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout="wide")

# ======================================================================
# Role presets
# ======================================================================

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

API_URL = "http://127.0.0.1:9999/chat"

# ======================================================================
# Layout: sidebar for config, main for chat
# ======================================================================

st.title("Multi AI Agent")

with st.sidebar:
    st.header("⚙️ Agent Configuration")

    # Role selection
    selected_role = st.selectbox(
        "Select agent role:",
        list(ROLE_PRESETS.keys()),
        index=0,
    )

    # Model selection
    selected_model = st.selectbox(
        "Select your AI model:",
        settings.ALLOWED_MODEL_NAMES,
    )

    # Web search toggle
    allow_web_search = st.checkbox("Allow web search", value=False)

    st.markdown("---")
    st.caption("You can edit the system prompt below in the main panel.")

# ======================================================================
# Main panel: system prompt, query, response
# ======================================================================

# Prefill system prompt from role preset, but allow editing
default_prompt = ROLE_PRESETS.get(selected_role, ROLE_PRESETS["General Assistant"])
system_prompt = st.text_area(
    "System prompt (agent instructions):",
    value=default_prompt,
    height=120,
)

user_query = st.text_area("Enter your query:", height=160)

col1, col2 = st.columns([1, 3])

with col1:
    ask_button = st.button("Ask Agent")

with col2:
    st.write("")  # small spacer

# ======================================================================
# Handle submission
# ======================================================================

if ask_button and user_query.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search,
    }

    try:
        logger.info("Sending request to backend")

        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

        else:
            logger.error(f"Backend error. Status code: {response.status_code}")
            st.error("Error communicating with backend. Please check the logs.")

    except Exception as e:
        logger.error("Error occurred while sending request to backend")
        st.error(str(CustomException("Failed to communicate to backend", error_detail=e)))
elif ask_button and not user_query.strip():
    st.warning("Please enter a query before asking the agent.")

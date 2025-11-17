"""
api.py
======

FastAPI backend for the **LLMOps Multi-AI Agent** project.

This module exposes a single `/chat` endpoint that allows clients to:

* Submit a model name, system prompt, message history, and search toggle.
* Validate the selected LLM against the project's allowed configuration.
* Invoke the LangGraph-powered agent via `get_response_from_ai_agents`.
* Return the final AI-generated response in a structured format.

The backend includes centralised logging, exception wrapping, and input
validation through Pydantic.
"""

# ======================================================================
# Imports
# ======================================================================

# FastAPI server framework + HTTP exception helper
from fastapi import FastAPI, HTTPException

# Pydantic model for validating incoming request bodies
from pydantic import BaseModel

# Type hint support for lists
from typing import List

# Core agent invocation function
from app.core.ai_agent import get_response_from_ai_agents

# Project configuration (allowed model names, API keys, etc.)
from app.config.settings import settings

# Logging utility (project-wide logging configuration)
from app.common.logger import get_logger

# Custom exception wrapper for structured error reporting
from app.common.custom_exception import CustomException


# ======================================================================
# Initialisation
# ======================================================================

# Create a logger specific to this module
logger = get_logger(__name__)

# Create the FastAPI application instance
app = FastAPI(title="MULTI AI AGENT")


# ======================================================================
# Request Schema
# ======================================================================

class RequestState(BaseModel):
    """
    Defines the expected request body for the `/chat` endpoint.

    Attributes
    ----------
    model_name : str
        The identifier of the LLM that the client wants to use.
    system_prompt : str
        System-level instructions that control the agent’s behaviour.
    messages : List[str]
        A list of user messages representing conversation history.
    allow_search : bool
        Whether to enable Tavily-based web search as a tool for the agent.
    """
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


# ======================================================================
# Chat Endpoint
# ======================================================================

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    Endpoint for querying the AI agent.

    Parameters
    ----------
    request : RequestState
        The structured request body containing model name, system prompt,
        conversation messages, and search toggle.

    Returns
    -------
    dict
        A JSON dictionary containing the `"response"` string produced by
        the AI agent.

    Raises
    ------
    HTTPException
        * 400 if the requested model name is invalid.
        * 500 if an internal error occurs during agent execution.
    """

    # --------------------------------------------------------------
    # Log received request
    # --------------------------------------------------------------
    logger.info(f"Received request for model: {request.model_name}")

    # --------------------------------------------------------------
    # Validate model selection
    # --------------------------------------------------------------
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name provided")
        raise HTTPException(status_code=400, detail="Invalid model name")

    # --------------------------------------------------------------
    # Process the chat request
    # --------------------------------------------------------------
    try:
        # Invoke the LangGraph-powered agent and capture the final response
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Successfully obtained response from model: {request.model_name}")

        # Return structured API response
        return {"response": response}

    # --------------------------------------------------------------
    # Global error handling
    # --------------------------------------------------------------
    except Exception as e:
        logger.error("An error occurred during AI response generation")
        raise HTTPException(
            status_code=500,
            detail=str(CustomException("Failed to get AI response", error_detail=e))
        )

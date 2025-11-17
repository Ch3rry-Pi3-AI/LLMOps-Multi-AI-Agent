"""
ai_agent.py
===========

Core interface for interacting with the Multi-AI Agent system.

This module builds a ReAct-style agent graph on top of **LangGraph** using
LangChain's stable **create_agent** API. The agent can optionally use
**Tavily** for web search.

Workflow:
* Load a Groq-backed chat model.
* Optionally attach a Tavily search tool.
* Build a LangGraph-powered agent via `langchain.agents.create_agent`.
* Invoke the agent with a messages state and return the final AI message.

This acts as the main execution layer for agent reasoning in the project.
"""

# ======================================================================
# Imports
# ======================================================================

# Groq LLM wrapper
from langchain_groq import ChatGroq

# Tavily search tool (recommended, stable package)
from langchain_tavily import TavilySearch

# Agent factory (builds a LangGraph agent graph under the hood)
from langchain.agents import create_agent

# Message type for filtering AI responses
from langchain_core.messages import AIMessage

# Project settings (API keys, allowed models, etc.)
from app.config.settings import settings


# ======================================================================
# Core Agent Function
# ======================================================================

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    """
    Generate a response using the LangGraph-backed ReAct-style AI agent.

    Parameters
    ----------
    llm_id : str
        The model identifier to load via the Groq API (ideally one of the
        allowed model names defined in project settings).
    query : list
        A list of message objects or message-like dictionaries representing the
        current conversation state to be passed into the agent graph.
    allow_search : bool
        Whether to enable Tavily web search as a tool for the agent.
    system_prompt : str
        A system-level instruction string that controls the agent's behaviour.

    Returns
    -------
    str
        The final text response produced by the last AI message in the sequence.

    Notes
    -----
    * If `allow_search` is True, a TavilySearch tool is attached (with a small
      max_results value for efficiency).
    * The agent itself is created via `langchain.agents.create_agent`, which
      compiles down to a LangGraph StateGraph under the hood.
    """

    # --------------------------------------------------------------
    # Initialise LLM
    # --------------------------------------------------------------

    # Create a Groq-backed LLM instance using the selected model ID
    llm = ChatGroq(model=llm_id)

    # --------------------------------------------------------------
    # Configure optional tools
    # --------------------------------------------------------------

    # If search is allowed, include the Tavily search tool; otherwise, no tools
    tools = [TavilySearch(max_results=2, topic="general")] if allow_search else []

    # --------------------------------------------------------------
    # Build the reasoning agent (LangGraph-powered)
    # --------------------------------------------------------------

    # Create a ReAct-style agent with tools and a system prompt
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    # --------------------------------------------------------------
    # Prepare agent input state
    # --------------------------------------------------------------

    # The agent expects messages wrapped inside a dict under the "messages" key
    state = {"messages": query}

    # --------------------------------------------------------------
    # Invoke the agent and collect results
    # --------------------------------------------------------------

    # Run the LangGraph-backed agent with the provided state
    response = agent.invoke(state)

    # Extract the list of returned message objects (AI + human + tool, etc.)
    messages = response.get("messages", [])

    # Filter out only AI-generated messages and grab their content
    ai_messages = [
        message.content
        for message in messages
        if isinstance(message, AIMessage)
    ]

    # Return the content of the last AI message
    return ai_messages[-1]

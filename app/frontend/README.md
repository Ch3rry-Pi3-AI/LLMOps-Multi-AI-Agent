# 🎨 **Frontend Folder — LLMOps Multi-AI Agent**

The `frontend` folder contains the **user interface layer** of the Multi-AI Agent system.
This layer provides a Streamlit-based UI that allows users to interact with the LangGraph-powered agent in a simple and accessible way.

It communicates directly with the FastAPI backend and acts as the visual entry point for the entire system.

## 📁 Current Contents

### **ui.py**

Implements the Streamlit interface for the Multi-AI Agent.
It provides:

* A text area for system prompt definition
* Model selection from the allowed Groq models
* A toggle for enabling Tavily-powered web search
* A query input area
* A button to send the request to the backend API
* Clean rendering of the agent’s final response

This file serves as the frontend interaction layer between the user and the core agent logic.

## 🎯 Purpose of the Frontend Layer

The frontend is designed to:

* Offer a simple UI for testing and interacting with the agent
* Communicate with the backend via REST
* Display AI-generated outputs cleanly and reliably

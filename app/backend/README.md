# 🖥️ **Backend Folder — LLMOps Multi-AI Agent**

The `backend` folder contains the FastAPI application layer for the Multi-AI Agent system.
It exposes HTTP endpoints that allow external clients (frontend, CLI tools, other services) to interact with the LangGraph-powered agent.

This layer is responsible for:

* Handling incoming API requests
* Validating inputs via Pydantic
* Routing requests to the core agent logic
* Returning structured, JSON-friendly responses
* Logging and error handling

## 📁 Current Contents

### **api.py**

Implements the FastAPI server for the project.
It includes:

* A `/chat` POST endpoint
* Request validation using `RequestState`
* Model name validation against `settings.ALLOWED_MODEL_NAMES`
* Invocation of the core agent (`get_response_from_ai_agents`)
* Centralised logging and structured error handling

This file acts as the public API interface for the entire system.

## 🔧 Purpose of the Backend Layer

The backend serves as the communication bridge between:

* The **core agent** (reasoning and tool usage)
* The **frontend** (UI or client applications)
* External processes or integrations

It ensures that all agent interactions follow a clean, documented, and secure request/response workflow.
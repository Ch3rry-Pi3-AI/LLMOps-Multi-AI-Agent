# 🚀 **Application Launcher — LLMOps Multi-AI Agent**

This branch introduces the unified application launcher for the Multi-AI Agent system.
The new file **`app/main.py`** starts both the FastAPI backend and the Streamlit frontend, enabling the entire system to run from a single entry point.

This simplifies development, testing, and usage by ensuring both services are brought online automatically and consistently.

## 🗂️ **Project Structure**

```text
LLMOPS-MULTI-AI-AGENT/
├── .venv/
├── .env
├── .gitignore
├── .python-version
├── llmops_multi_ai_agent.egg-info/
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.py
├── uv.lock
│
└── app/
    ├── main.py                          # NEW: Unified launcher for backend + frontend
    ├── backend/
    ├── common/
    ├── config/
    ├── core/
    └── frontend/
```

## 🧩 **What Was Added in This Branch**

### ✔️ `app/main.py`

This module provides a fully integrated start-up routine for the Multi-AI Agent. It includes:

* A threaded launcher for the FastAPI backend
* A Streamlit launcher for the frontend UI
* Logging for start-up events and failures
* Structured exception handling via `CustomException`
* Environment variable loading via `load_dotenv`
* A single execution point for running the entire application

This design ensures that both components (backend + frontend) start in the correct order and operate concurrently without requiring two separate terminal sessions.

## 🎯 **Purpose of This Branch**

To consolidate application start-up into one central location, enabling:

* A single command to run the full system
* Cleaner development workflows
* Reduced overhead in managing backend/frontend services
* A predictable and unified start-up sequence

This approach will be especially useful as the project grows into multi-agent orchestration, deployment workflows, and UI expansion.

## ✅ **Summary**

This branch adds the project’s unified launcher:

* Automatically starts backend (Uvicorn) + frontend (Streamlit)
* Includes logging and error handling
* Simplifies usage and development of the Multi-AI Agent

The system can now be launched cleanly from a single file, making it easier to run and test the entire project end-to-end.

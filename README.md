# 🎨 **Frontend UI Layer — LLMOps Multi-AI Agent**

This branch introduces the first frontend interface for the Multi-AI Agent system.
The new file **`app/frontend/ui.py`** provides a Streamlit-based user interface that allows users to interact directly with the FastAPI backend and, through it, the LangGraph-powered agent.

This frontend acts as the system’s visual interaction layer and offers an accessible way to test, query, and evaluate the agent’s reasoning capabilities.

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
    ├── main.py
    ├── backend/
    ├── common/
    ├── config/
    ├── core/
    └── frontend/
        └── ui.py                       # NEW: Streamlit interface for agent interaction
```

## 🧩 **What Was Added in This Branch**

### ✔️ `app/frontend/ui.py`

This module introduces the project’s first graphical interface. It provides:

* A Streamlit layout for defining a system prompt
* A dropdown for selecting supported Groq models
* A toggle for enabling Tavily-powered web search
* A text area for the user’s query
* A button to send structured requests to the FastAPI `/chat` endpoint
* Rendering of the agent’s final response
* Logging of frontend → backend communication events

This file enables hands-on interaction with the agent without requiring command-line tools or manual API calls.

## 🎯 **Purpose of This Branch**

To introduce a simple yet functional frontend layer that:

* Makes the agent accessible through a graphical UI
* Bridges user input with backend logic
* Provides real-time feedback via a clean and minimal interface
* Supports debugging and experiment workflows during development

This frontend will be extended in future branches to include chat history, better formatting, multi-agent controls, and richer UI components.

## ✅ **Summary**

This branch adds the project’s first user-facing component:

* Streamlit UI for interacting with the agent
* Clean layout for prompts, model selection, and queries
* Backend integration with structured request and response handling

The Multi-AI Agent can now be interacted with through a simple and intuitive web interface.

# 🤖 **LLMOps Multi-AI Agent — Project Overview**

This repository presents a complete **LLMOps workflow** for a **Multi-AI Agent chatbot**, powered by **Groq LLMs**, optional **Tavily web search**, and a clean **FastAPI + Streamlit** architecture.
It extends beyond local experimentation into a full **CI/CD pipeline** with:

* **Jenkins (Docker-in-Docker)**
* **SonarQube code-quality analysis**
* **AWS Elastic Container Registry (ECR) for image storage**
* **AWS ECS Fargate** for serverless container deployment

From a single UI, users can select roles (e.g. technical expert, journalist), choose LLM models, toggle web search, and interact with the agent — all backed by a production-style MLOps stack.

<p align="center">
  <img src="img/streamlit/streamlit_app.gif" alt="Multi-AI Agent Streamlit Demo" width="100%">
</p>

## 🧩 **Grouped Stages**

|     #     | Stage                                    | Description                                                                                                                                                                                                                                                       |
| :-------: | :--------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   **00**  | **Project Setup**                        | Established the base VS Code structure, virtual environment, `.env` secrets, logging and exception utilities, and configuration settings for API keys and model selection.                                                                                        |
|   **01**  | **WSL & Ubuntu Environment**             | Installed **WSL** and **Ubuntu** on Windows, configured Docker Engine inside Ubuntu, and prepared a Linux-based development environment for containers and CI tooling.                                                                                            |
| **02–04** | **Core Multi-AI Agent Logic**            | Implemented the Groq-backed LangGraph agent (`ai_agent.py`), a **FastAPI** backend API for the `/chat` endpoint, and an initial **Streamlit** UI for sending queries, selecting models, and toggling web search.                                                  |
|   **05**  | **Unified Application Launcher**         | Added a single `main.py` entry point to start both the Uvicorn backend and the Streamlit frontend together, enabling end-to-end app execution with one command.                                                                                                   |
|   **06**  | **Jenkins Setup (Docker-in-Docker)**     | Built a custom **Jenkins DinD** image, installed Docker and Python inside the container, and configured Jenkins to run in WSL with full Docker access for building images.                                                                                        |
|   **07**  | **GitHub Integration with Jenkins**      | Generated a GitHub personal access token, added it as credentials in Jenkins, created a Pipeline job, and wired a **Jenkinsfile** so Jenkins can clone the repository and run pipeline stages from source control.                                                |
|   **08**  | **SonarQube Code Quality Integration**   | Deployed **SonarQube** via Docker, installed Sonar plugins in Jenkins, configured a scanner and server connection, added a SonarQube analysis stage to the Jenkinsfile, and inspected code quality reports in the SonarQube UI.                                   |
|   **09**  | **AWS ECR – Build & Push Docker Images** | Installed AWS CLI in Jenkins, created an IAM user and ECR repository, added AWS credentials to Jenkins, and implemented a pipeline stage that builds the project Docker image and pushes it to **Amazon ECR**.                                                    |
|   **10**  | **AWS ECS Fargate Deployment**           | Created an ECS Fargate cluster and task definition pointing to the ECR image, configured ports and environment variables, updated security groups, and added a final Jenkins stage to trigger **ECS service updates**, exposing the Streamlit UI via a public IP. |

## 🗂️ **Project Structure**

```text
LLMOPS-MULTI-AI-AGENT/
├── Dockerfile                         # 🐳 Builds the Multi-AI Agent app image (backend + frontend)
├── Jenkinsfile                        # ⚙️ Jenkins CI/CD pipeline (SonarQube, ECR build/push, ECS deploy)
├── custom_jenkins/                    # 🧱 Custom Jenkins DinD image definition
│   └── Dockerfile                     # Docker-in-Docker Jenkins image with Docker + AWS CLI installed
├── img/                               # 📸 Screenshots and GIFs for documentation
├── .venv/                             # Local Python virtual environment (managed via uv / venv)
├── .env                               # 🔐 Environment variables (GROQ_API_KEY, TAVILY_API_KEY, etc.)
├── .gitignore                         # Ignore rules for venv, logs, artefacts, and OS files
├── .python-version                    # Python version pin for consistent environments
├── llmops_multi_ai_agent.egg-info/    # 📦 Auto-generated packaging metadata
├── pyproject.toml                     # 🧩 Project metadata, dependencies, and build configuration
├── README.md                          # 📖 Main project documentation (you are here)
├── requirements.txt                   # 📦 Python dependencies (FastAPI, Streamlit, LangChain, Groq, etc.)
├── setup.py                           # 🔧 Editable install configuration for packaging
├── uv.lock                            # 🔒 Exact dependency lockfile generated by uv
│
└── app/                               # 🧠 Application package (backend, frontend, core agent)
    ├── main.py                        # 🚀 Unified launcher that starts backend (Uvicorn) + frontend (Streamlit)
    ├── backend/                       # 🌐 Backend API layer (FastAPI)
    │   └── api.py                     # `/chat` endpoint: validates requests, calls AI agent, handles errors
    ├── common/                        # 🪵 Shared utilities for reliability and observability
    │   ├── custom_exception.py        # Rich `CustomException` class with file/line context for errors
    │   └── logger.py                  # Centralised logging setup for console and structured logs
    ├── config/                        # ⚙️ Configuration and environment management
    │   └── settings.py                # Loads API keys, allowed model names, and global settings from `.env`
    ├── core/                          # 🧠 Core reasoning logic
    │   └── ai_agent.py                # LangGraph/Groq-based ReAct-style agent with optional Tavily search
    └── frontend/                      # 🎨 User-facing UI layer
        └── ui.py                      # Streamlit web UI: roles, model selection, web search toggle, chat interface
```

## 🚀 **Summary**

The **LLMOps Multi-AI Agent** project shows how to take a modern LLM-powered application from **local prototype** to a **production-style cloud deployment pipeline**.

It combines:

* A Groq-backed, LangGraph-powered multi-AI agent with optional Tavily web search
* A clean split between **FastAPI backend** and **Streamlit frontend**
* Robust logging and exception handling for better debuggability
* **Jenkins (Docker-in-Docker)** for CI orchestration
* **SonarQube** for continuous code-quality analysis
* **AWS ECR** for container image storage
* **AWS ECS Fargate** for serverless, scalable deployment behind a public IP

Together, these stages form a complete **LLMOps / DevOps story**:
from writing a prompt in the Streamlit UI, through CI quality gates and container builds, all the way to running the chatbot as a managed service in the cloud.

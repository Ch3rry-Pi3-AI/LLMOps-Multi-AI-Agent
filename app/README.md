# 📦 **App Folder — LLMOps Multi-AI Agent**

The `app` directory contains the entire operational logic of the Multi-AI Agent system.
It serves as the central application layer, bringing together backend services, frontend UI, core agent reasoning, configuration management, and shared utilities.

This folder is the heart of the project, and all user-facing and system-facing functionality flows through one or more of its submodules.

## 📁 Folder Overview

### **main.py**

The unified application launcher.
It starts both the FastAPI backend and the Streamlit frontend, ensuring the full system runs from a single entry point.

### **backend/**

Contains the FastAPI server that exposes the `/chat` endpoint used by the frontend or any external client to query the agent.

### **frontend/**

Provides the Streamlit user interface for interacting with the agent in a visual and accessible way.

### **core/**

Houses the core reasoning logic, including the LangGraph-powered agent that generates intelligent responses.

### **config/**

Manages environment variables, model configuration, and global application settings.

### **common/**

Provides shared utilities such as logging and custom exception handling used across all modules.

## 🎯 Purpose of the `app` Layer

The `app` folder unifies:

* Core agent reasoning
* Backend API serving
* Frontend user interaction
* Centralised configuration
* Shared utilities and infrastructure

Every high-level action the system performs — from receiving a user query, to reasoning with tools, to presenting an answer — is coordinated through this layer.
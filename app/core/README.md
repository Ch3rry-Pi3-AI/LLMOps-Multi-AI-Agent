# 🧠 **Core Folder — LLMOps Multi-AI Agent**

The `core` folder contains the **main reasoning and orchestration logic** for the Multi-AI Agent system.
Modules in this folder define how the agent processes user input, interacts with tools, performs reasoning steps, and returns structured responses.

This layer sits above the low-level utilities (`common/`) and the configuration system (`config/`).
It represents the **brain of the application**, where agent workflows and decision-making pipelines are implemented.

## 📁 Current Contents

### **ai_agent.py**

Implements the primary agent execution function.
It:

* Loads the selected Groq LLM
* Optionally enables TavilySearch for real-time web retrieval
* Builds a ReAct-style agent graph using LangGraph (via `create_agent`)
* Executes agent reasoning with a message-based state
* Returns the final AI-generated message

This file acts as the main entry point for all agent reasoning tasks.

## 🔧 Purpose of the Core Layer

The `core` folder is responsible for:

* Building and invoking LangGraph agent workflows
* Managing the high-level logic for multi-agent operations
* Handling how tools and LLMs interact inside the reasoning loop
* Preparing outputs for the rest of the application
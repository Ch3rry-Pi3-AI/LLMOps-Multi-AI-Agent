# `common/` README — Core Utilities (Custom Exception & Logger)

This folder contains the **shared utility modules** used throughout the **LLMOps Multi AI Agent** project.
They provide lightweight, reusable components for **error handling** and **logging**, ensuring consistent debugging, traceability, and reliability across all pipelines, services, and LLM workflows.

## 📁 Folder Overview

```text
src/common/
├─ __init__.py           # Marks the directory as a package
├─ custom_exception.py   # Unified and detailed exception handling
└─ logger.py             # Centralised logging configuration
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Implements a `CustomException` class that enriches Python exceptions with detailed debugging context — including the **file name**, **line number**, and traceback of the original error.

### Key Features

* Standardises exception handling across the entire Multi AI Agent codebase.
* Automatically collects error metadata via `sys.exc_info()` if not explicitly provided.
* Useful in all core pipelines — ingestion, processing, modelling, API routes, or orchestration components.

### Example Usage

```python
from common.custom_exception import CustomException
import sys

try:
    raise ValueError("Invalid input format.")
except Exception as e:
    raise CustomException("Pipeline execution error", sys) from e
```

### Output Example

```
Error in /multi-ai-agent/common/example.py, line 8: Pipeline execution error
Traceback (most recent call last):
  File "/multi-ai-agent/common/example.py", line 8, in <module>
    raise ValueError("Invalid input format.")
ValueError: Invalid input format.
```

## 🪵 `logger.py` — Centralised Logging

### Purpose

Provides a unified logging setup shared by all modules in the Multi AI Agent project.
Each log entry is timestamped and written to a daily rotating log file inside the `logs/` directory.

### Log File Format

* Directory: `logs/`
* File name: `log_YYYY-MM-DD.log`
* Example: `logs/log_2025-11-10.log`

### Example Usage

```python
from common.logger import get_logger

logger = get_logger(__name__)
logger.info("Initialising Multi AI Agent pipeline.")
logger.warning("Missing fields detected in training data.")
logger.error("Model failed to load due to missing checkpoint.")
```

### Output Example

```
2025-11-10 19:42:01,120 - INFO - Initialising Multi AI Agent pipeline.
2025-11-10 19:42:01,381 - WARNING - Missing fields detected in training data.
2025-11-10 19:42:01,645 - ERROR - Model failed to load due to missing checkpoint.
```

## ✅ Summary

* `custom_exception.py` ensures consistent and informative error reporting.
* `logger.py` provides a reliable, timestamped logging system for all components.
* Together with `__init__.py`, these modules form the **core reliability layer** underpinning all Multi AI Agent pipelines and services.

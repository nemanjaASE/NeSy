---
title: 🚀 FastAPI
nav_order: 6
---

# 🚀 FastAPI

## 📋 Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (manages Python 3.12 for you — no separate Python install needed)
- Neo4j AuraDB (or a local Neo4j Desktop instance)
- Groq Cloud API Key (or a local LLM model API KEY)

## 🛠️ Installation & Setup

### **0. Clone the repository**

```
 git clone https://github.com/nemanjaASE/NeSy-X.git
```

### **1. Navigate to the backend project root:**

```
  cd NeSy-X/backend
```

### **2. Install `uv`:**

This project uses [`uv`](https://docs.astral.sh/uv/) to manage the virtual environment and pin exact dependency versions (`uv.lock`), so every clone reproduces the same environment. `uv` also downloads and manages the required **Python 3.12** for you — you do not need Python pre-installed at all.

Use the standalone installer (does not require an existing Python):

- **macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

> **Note:** If you already have a working Python + pip, `pip install uv` also works. Avoid this on older Linux systems with an outdated system Python (missing SSL support, etc.) — use the standalone installer above instead, since it has no Python dependency. If you specifically want a system-managed Python 3.12 for reasons outside this project, **pyenv** is still a fine option: 📘 **[pyenv Setup Guide](./pyenv-python312-ubuntu.md)**.

### **3. Install dependencies:**

```bash
uv sync
```

This creates a `.venv` in `backend/` and installs the exact versions pinned in `uv.lock`. Run commands through `uv run <command>` (e.g. `uv run fastapi dev app/main.py`), or activate the environment the usual way:

- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

### **Adding a new dependency**

1. `uv add <package-name>` (or `uv add --optional dev <package-name>` for a dev-only tool like a linter). This installs it and updates `pyproject.toml` and `uv.lock` for you.
2. Commit both `pyproject.toml` and `uv.lock`.

### **4. Configuration (.env file):**

Create a .env file in the backend/ directory:

```
# Environment variables for the Neuro-symbolic Diagnostic API
PROJECT_NAME="your-project-name"
ENVIRONMENT="environment-name" # e.g., development or production

# Neo4j connection settings
NEO4J_URL="your-neo4j-url"
NEO4J_USERNAME="your-neo4j-username"
NEO4J_PASSWORD="your-neo4j-password"

# LLM API settings
LLM_API_KEY="your-llm-api-key"
LLM_EXTRACTION_MODEL_NAME="your-llm-extraction-model-name"
LLM_XAI_MODEL_NAME="your-llm-xai-model-name"

# Embedding model
EMBEDDING_MODEL_NAME="your-embedding-model-name"

# CORS settings
ALLOWED_ORIGINS="your-allowed-origins" # e.g., http://localhost:3000
ALLOWED_METHODS="your-allowed-methods" # e.g., GET,POST,PUT,DELETE
ALLOWED_HEADERS="your-allowed-headers" # e.g., Content-Type,Authorization
ALLOW_CREDENTIALS="your-allow-credentials" # true or false
```

## 💻 Running the Application

### **1. Initialize the Knowledge Graph:**

Before starting the API, you must populate the Neo4j database with the medical ontologies, calculate the Information Content (IC) weights, and generate symptom embeddings.

> **Note:** The preparation pipeline is currently implemented as interactive Jupyter Notebooks.
> 📘 **[Click here to read the detailed Notebooks Setup Guide](./notebooks.md)** to learn how to configure your VS Code kernel and execute the graph enrichment steps.

### **2. Start the FastAPI Development Server**

```bash
uv run fastapi dev app/main.py
```

## 🧪 Local Testing & CI Checks

Before pushing code or creating a pull request, it is highly recommended to replicate the GitHub Actions CI pipeline locally. This ensures your code is clean, type-safe, and secure.

### 1. Install Dev Dependencies

Install the necessary testing and linting tools alongside the main dependencies:

```bash
uv sync --extra dev
```

### 2. Set Up `pre-commit` Hooks

The repo ships a `.pre-commit-config.yaml` (repo root) that runs Ruff and basic file hygiene checks automatically on every `git commit`, so issues are caught before they even reach CI. Install the git hook once per clone:

```bash
uv run pre-commit install
```

Run it manually against everything (e.g. after pulling a large change):

```bash
uv run pre-commit run --all-files
```

> **Note:** `pre-commit` is a local, best-effort safety net — it doesn't replace CI. `backend-ci.yml` runs the same Ruff checks (plus mypy/bandit/pip-audit) on every push/PR regardless of whether hooks are installed locally.

### 3. Linting & Formatting (Ruff)

We use Ruff for fast code linting and formatting.

```bash
# Check for styling and logic errors
uv run ruff check .

# Auto-format the code
uv run ruff format .
```
### 4. Static Type Checking (Mypy)

Ensure all type hints are correct:

```bash
uv run mypy app/
```

### 5. Security Audits

Scan both the application code and external libraries for known vulnerabilities:

```bash
# Scan application code for bad practices
uv run bandit -r app/

# Audit dependencies for known CVEs
uv run pip-audit
```

---

**⬅ Previous:** [🦙 Ollama — Setup Guide](./ollama_setup.md) &nbsp;|&nbsp; **Next ➡:** [🧪 Testing the Natural Language Processing Layer](./nlp-test.md)

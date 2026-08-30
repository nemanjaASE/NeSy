---
title: 🚀 FastAPI
nav_order: 6
---

# 🚀 FastAPI

## 📋 Prerequisites

- Python 3.12+
- Neo4j AuraDB (or a local Neo4j Desktop instance)
- Groq Cloud API Key (or a local LLM model API KEY)

## 🛠️ Installation & Setup

### **0. Clone the repository**

```
 git clone https://github.com/nemanjaASE/NeSy.git
```

### **1. Navigate to the backend project root:**

```
  cd NeSy/backend
```

### **2. Create a virtual environment:**

#### 🖥️ Windows

```powershell
python -m venv .venv

# Activate venv
.venv\Scripts\activate
```

#### 🍎 macOS

```bash
python3 -m venv .venv

# Activate venv
source .venv/bin/activate
```

#### 🐧 Linux

```bash
python3 -m venv .venv

# Activate venv
source .venv/bin/activate
```

> **⚠️ Note:** This project requires **Python 3.12**. Most Linux systems ship with an older version that may also lack SSL support, causing `pip` to fail during dependency installation. It is strongly recommended to use **pyenv** to install and manage Python 3.12 before proceeding with the steps below.
>
> 📘 **[Click here to read the pyenv Setup Guide](../docs/pyenv-python312-ubuntu.md)**

### **3. Install dependencies:**

```
  pip install -r requirements.txt
```

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
> 📘 **[Click here to read the detailed Notebooks Setup Guide](./notebooks/README.md)** to learn how to configure your VS Code kernel and execute the graph enrichment steps.

### **2. Start the FastAPI Development Server**

```
fastapi dev app/main.py
```

## 🧪 Local Testing & CI Checks

Before pushing code or creating a pull request, it is highly recommended to replicate the GitHub Actions CI pipeline locally. This ensures your code is clean, type-safe, and secure.

### 1. Install Dev Dependencies

Install the necessary testing and linting tools alongside the main requirements:

```
pip install ruff mypy bandit pip-audit
```

### 2. Linting & Formatting (Ruff)

We use Ruff for fast code linting and formatting.

```
# Check for styling and logic errors
ruff check .

# Auto-format the code
ruff format .
```
### 3. Static Type Checking (Mypy)

Ensure all type hints are correct:

```
mypy app/
```

### 4. Security Audits

Scan both the application code and external libraries for known vulnerabilities:

```
# Scan application code for bad practices
bandit -r app/

# Audit dependencies for known CVEs
pip-audit -r requirements.txt
```

# 🚀 Getting Started

## 📋 Prerequisites

- Python 3.12+
- Neo4j AuraDB (or a local Neo4j Desktop instance)
- Groq Cloud API Key (or a local LLM model API KEY)

## 🛠️ Installation & Setup

**0. Clone the repository**

```
 git clone https://github.com/nemanjaASE/NeSy.git
```

**1. Navigate to the backend project root:**

```
  cd NeSy/backend
```

**2. Create a virtual environment:**

```
  python -m venv .venv

  # Activate on Windows:
  .venv\Scripts\activate
  # Activate on Linux/macOS:
  source .venv/bin/activate
```

**3. Install dependencies:**

```
  pip install -r requirements.txt
```

**4. Configuration (.env file):**

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

**1. Initialize the Knowledge Graph:**

Before starting the API, you must populate the Neo4j database with the medical ontologies, calculate the Information Content (IC) weights, and generate symptom embeddings. 

> **Note:** The preparation pipeline is currently implemented as interactive Jupyter Notebooks. 
> 📘 **[Click here to read the detailed Notebooks Setup Guide](./notebooks/README.md)** to learn how to configure your VS Code kernel and execute the graph enrichment steps.

**2. Start the FastAPI Development Server**

```
fastapi dev app/main.py
```

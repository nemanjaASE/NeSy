---
title: 📚 Notebook Directory & Workflow
nav_order: 3
---

# 📚 Notebook Directory & Workflow

The notebooks in this directory live in two folders: `pipeline/` (the actual NeSy-X workflow — data enrichment plus the neural/symbolic/XAI layer notebooks, each with its own `tests/` fixtures) and `demos/` (standalone visual aids that are not part of the framework's execution flow).

## ⚙️ 1. `pipeline/` — Data Enrichment
These notebooks must be executed to "bake" the logic and weights into the Neo4j graph. Run these if you are not using a pre-configured database dump.

| Notebook | Purpose | Impact on Database |
|---|---|---|
| `pipeline/calculate-weights.ipynb` | Calculates Information Content (IC) for each symptom based on disease frequency. | Adds `weight` property to `:Symptom` nodes. |
| `pipeline/generate-embeddings.ipynb` | Generates high-dimensional vectors using the `multilingual-e5-large` model. | Adds `embedding` property to `:Symptom` nodes. |

## 🧪 2. `pipeline/` — Layer Demonstrations (Individual Components)

These notebooks are used for research, validation, and testing each layer of the NeSy framework in isolation, reading fixtures from `pipeline/tests/`. They do not modify the database.

- `pipeline/nlp-llm.ipynb` (Neural Layer)

  - **Focus**: Symptom extraction.
    
  - **Action**: Demonstrates how an LLM parses unstructured user inputs into structured symptom lists.

- `pipeline/inference-and-scoring.ipynb` (Symbolic Layer)

  - **Focus**: Graph reasoning and ranking.

  - **Action**: Executes the hybrid Vector Search + Normalized Weighted Sum scoring directly against Neo4j to rank potential diseases.

- `pipeline/xai-llm.ipynb` (Neural Layer)

  - **Focus**: Clinical transparency.

  - **Action**: Takes raw inference results and generates natural language explanations, bridging the gap between numbers and human-readable diagnostics.

## 🎨 3. `demos/` — Visual Aids

Standalone notebooks that support exploration and reporting but are not required to run the framework.

- `demos/embeddings-visualization.ipynb` — projects symptom embeddings into 2D (t-SNE + K-Means) for an interactive Plotly view of the vector space. Writes to `demos/results/`.

# ⚙️ Setting Up the Local Jupyter Kernel

Since this folder has its own dedicated environment, follow these steps to ensure VS Code uses the correct dependencies.

## 🛠️ Option 1: Manual Setup (Step-by-Step)

**1. Navigate to the `notebooks/` directory:**

```
  cd NeSy/notebooks
```

**2. Create a virtual environment:**

```
  python -m venv .venv
```

**3. Activate virtual environment:**

- Windows
  ```
    .venv\Scripts\activate
  ```
- macOS/Linux
  ```
    source .venv/bin/activate
  ```

**3. Install dependencies:**

```
  pip install -r requirements.txt
```

**4. Install Jupyter kernel:**

```
  python -m ipykernel install --user --name=nesy-notebooks --display-name="NeSy Notebooks (venv)"
```

**5. Select the Kernel in VS Code:**

1. Open any `.ipynb` file.
2. Click **Select Kernel** in the top-right corner.
3. Navigate to **Jupyter Kernel** ->  **NeSy Notebooks (venv)**.

> **Note:** If the kernel does not appear immediately, restart VS Code and try selecting the kernel again.

## 🤖  Option 2: Automated Setup (One-Click Script)

We’ve included ready-to-run setup scripts in this folder — just double-click or run them to install everything automatically.

---
 
### 🖥️ Windows
 
**Option A: Double-click (easiest)**
 
1. Find `setup.bat` in the `notebooks/` folder
2. Double-click it — it will automatically:
   - Create `.venv`
   - Install dependencies
   - Register the Jupyter kernel
   - Show you next steps
     
**Option B: Run from terminal**
 
```
setup.bat
```
 
---
 
### 🍎 macOS
 
**Option A: Double-click (easiest)**
 
1. Find `setup.sh` in the `notebooks/` folder
2. Right-click → **Open With** → **Terminal**
   
**Option B: Run from terminal**
 
```bash
chmod +x setup.sh
./setup.sh
```
 
---
 
### 🐧 Linux
 
**Run from terminal:**
 
```bash
chmod +x setup.sh
./setup.sh
```
 
> **Note:** `chmod +x` is only needed once to make the script executable. On macOS and Linux, both platforms use the same `setup.sh` script.
 
---
 
💡 No need to edit or create anything — scripts are pre-configured for this project.

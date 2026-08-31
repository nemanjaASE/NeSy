---
title: 📚 Notebook Directory & Workflow
nav_order: 4
---

# 📚 Notebook Directory & Workflow

The notebooks in this directory live in two folders: `pipeline/` (the actual NeSy-X workflow, split into `preparation/` and `execution/` phases matching the framework's own two-phase design) and `demos/` (standalone visual aids that are not part of the framework's execution flow).

## ⚙️ 1. `pipeline/preparation/` — Data Enrichment
These notebooks must be executed to "bake" the logic and weights into the Neo4j graph. Run these if you are not using a pre-configured database dump.

| Notebook | Purpose | Impact on Database |
|---|---|---|
| `preparation/01-calculate-weights.ipynb` | Calculates Information Content (IC) for each symptom based on disease frequency. | Adds `weight` property to `:Symptom` nodes. |
| `preparation/02-generate-embeddings.ipynb` | Generates high-dimensional vectors using the `multilingual-e5-large` model. | Adds `embedding` property to `:Symptom` nodes. |

## 🧪 2. `pipeline/execution/` — Layer Demonstrations (Individual Components)

These notebooks are used for research, validation, and testing each layer of the NeSy framework in isolation, reading fixtures from `execution/tests/`. They do not modify the database, and are numbered in the same order as the framework's Execution Phase steps.

- `execution/01-nlp-llm.ipynb` (Neural Layer)

  - **Focus**: Symptom extraction.

  - **Action**: Demonstrates how an LLM parses unstructured user inputs into structured symptom lists.

- `execution/02-semantic-mapping.ipynb` (Neural Layer)

  - **Focus**: Mapping extracted symptoms to ontology concepts.

  - **Action**: Embeds symptoms with `multilingual-e5-large` and matches them against ontological symptom embeddings via cosine similarity. Saves the mapped symptoms for the next notebook.

- `execution/03-inference-and-scoring.ipynb` (Symbolic Layer)

  - **Focus**: Graph reasoning and ranking.

  - **Action**: Loads the symptoms mapped by `02-semantic-mapping.ipynb` and executes the IC-weighted, normalized scoring query against Neo4j to rank candidate diseases.

- `execution/04-xai-llm.ipynb` (Neural Layer)

  - **Focus**: Clinical transparency.

  - **Action**: Takes raw inference results and generates natural language explanations, bridging the gap between numbers and human-readable diagnostics.

## 🎨 3. `demos/` — Visual Aids

Standalone notebooks that support exploration and reporting but are not required to run the framework.

- `demos/embeddings-visualization.ipynb` — projects symptom embeddings into 2D (t-SNE + K-Means) for an interactive Plotly view of the vector space. Writes to `demos/results/`.
- `demos/embedding-similarity.ipynb` — visualizes the cosine similarity behind the semantic-mapping threshold: the angle between two term embeddings, and a PCA projection of related/unrelated terms around a shared anchor. Writes to `demos/results/`.

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

{: .note }
If the kernel does not appear immediately, restart VS Code and try selecting the kernel again.

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

{: .note }
`chmod +x` is only needed once to make the script executable. On macOS and Linux, both platforms use the same `setup.sh` script.

---

💡 No need to edit or create anything — scripts are pre-configured for this project.

---

**⬅ Previous:** [🧬 Biomedical Ontologies and Graph Representation](./ontology.md) &nbsp;|&nbsp; **Next ➡:** [🦙 Ollama — Setup Guide](./ollama_setup.md)

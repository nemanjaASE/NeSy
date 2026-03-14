# 📓 Preparation pipeline

This directory contains the tools to transform a raw Neo4j medical graph into an AI-ready Knowledge Graph. These notebooks handle the mathematical weighting and vectorization of symptoms.

## ⚙️ Setting Up the Local Jupyter Kernel

Since this folder has its own dedicated environment, follow these steps to ensure VS Code uses the correct dependencies.

### 🛠️ Option 1: Manual Setup (Step-by-Step)

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

### 🤖  Option 2: Automated Setup (One-Click Script)

We’ve included ready-to-run setup scripts in this folder — just double-click or run them to install everything automatically.

🖥️ For Windows

1. Open the `notebooks/` folder.
  
2. Double-click `setup.bat` — it will:
    - Create .venv
    - Install dependencies
    - Register the Jupyter kernel
    - Show you next steps

💡 No need to edit or create anything — script is pre-configured for this project.

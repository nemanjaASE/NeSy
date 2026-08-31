#!/bin/bash
echo ""
echo "========================================"
echo "  NeSy Notebooks - Setup Script"
echo "========================================"
echo ""

if ! command -v uv &> /dev/null; then
  echo "[ERROR] uv is not installed or not in PATH."
  echo "Install it with:"
  echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
  echo "Then restart this terminal and re-run this script."
  exit 1
fi

echo "uv version: $(uv --version)"
echo ""

echo "[1/3] Installing dependencies (uv downloads Python 3.12 automatically if needed)..."
uv sync --extra dev
if [ $? -ne 0 ]; then
  echo "[ERROR] Failed to install dependencies."
  exit 1
fi
echo "[✓] Dependencies installed."
echo ""

echo "[2/3] Installing Jupyter kernel..."
uv run python -m ipykernel install --user --name=nesy-notebooks --display-name="NeSy Notebooks (venv)"
if [ $? -ne 0 ]; then
  echo "[ERROR] Failed to install Jupyter kernel."
  exit 1
fi
echo "[✓] Jupyter kernel installed."
echo ""

echo "[3/3] Setup complete!"
echo ""
echo "========================================"
echo "  Next Steps:"
echo "========================================"
echo "1. Open VS Code"
echo "2. Open any .ipynb file"
echo "3. Click 'Select Kernel' (top-right)"
echo "4. Choose 'NeSy Notebooks (venv)'"
echo ""
echo "If the kernel doesn't appear, restart VS Code."
echo "========================================"
echo ""

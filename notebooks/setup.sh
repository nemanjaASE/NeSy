#!/bin/bash
echo ""
echo "========================================"
echo "  NeSy Notebooks - Setup Script"
echo "========================================"
echo ""

if ! command -v python3 &> /dev/null; then
  echo "[ERROR] Python is not installed or not in PATH."
  echo "Please install Python from https://www.python.org/"
  exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.12"

if [ "$PYTHON_VERSION" != "$REQUIRED_VERSION" ]; then
  echo "[ERROR] Python $REQUIRED_VERSION is required, but found Python $PYTHON_VERSION."
  echo ""
  echo "Please install Python 3.12 and try again."
  echo "On Linux, it is recommended to use pyenv:"
  echo "  https://github.com/nemanjaASE/NeSy/blob/main/docs/pyenv-python312-ubuntu.md"
  exit 1
fi

echo "Python version: $(python3 --version)"
echo ""
echo "[1/5] Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
  echo "[ERROR] Failed to create virtual environment."
  exit 1
fi
echo "[✓] Virtual environment created."
echo ""

echo "[2/5] Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
  echo "[ERROR] Failed to activate virtual environment."
  exit 1
fi
echo "[✓] Virtual environment activated."
echo ""

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "[ERROR] Failed to install dependencies."
  exit 1
fi
echo "[✓] Dependencies installed."
echo ""

echo "[4/5] Installing Jupyter kernel..."
python -m ipykernel install --user --name=nesy-notebooks --display-name="NeSy Notebooks (venv)"
if [ $? -ne 0 ]; then
  echo "[ERROR] Failed to install Jupyter kernel."
  exit 1
fi
echo "[✓] Jupyter kernel installed."
echo ""

echo "[5/5] Setup complete!"
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
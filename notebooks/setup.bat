@echo off
echo.
echo ========================================
echo   NeSy Notebooks - Setup Script
echo ========================================
echo.

where uv >nul 2>&1
if errorlevel 1 (
  echo [ERROR] uv is not installed or not in PATH.
  echo Install it with:
  echo   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  echo Then restart this terminal and re-run this script.
  pause
  exit /b 1
)

echo uv found:
uv --version
echo.

echo [1/3] Installing dependencies (uv downloads Python 3.12 automatically if needed)...
uv sync --extra dev
if errorlevel 1 (
  echo [ERROR] Failed to install dependencies.
  pause
  exit /b 1
)
echo [OK] Dependencies installed.
echo.

echo [2/3] Installing Jupyter kernel...
uv run python -m ipykernel install --user --name=nesy-notebooks --display-name="NeSy Notebooks (venv)"
if errorlevel 1 (
  echo [ERROR] Failed to install Jupyter kernel.
  pause
  exit /b 1
)
echo [OK] Jupyter kernel installed.
echo.

echo [3/3] Setup complete!
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo 1. Open VS Code
echo 2. Open any .ipynb file
echo 3. Click "Select Kernel" (top-right)
echo 4. Choose "NeSy Notebooks (venv)"
echo.
echo If the kernel doesn't appear, restart VS Code.
echo ========================================
echo.
pause

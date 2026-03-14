@echo off
echo.
echo ========================================
echo   NeSy Notebooks - Setup Script
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo [✓] Virtual environment created.
echo.

echo [2/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [✓] Virtual environment activated.
echo.

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [✓] Dependencies installed.
echo.

echo [4/5] Installing Jupyter kernel...
python -m ipykernel install --user --name=nesy-notebooks --display-name="NeSy Notebooks (venv)"
if errorlevel 1 (
    echo [ERROR] Failed to install Jupyter kernel.
    pause
    exit /b 1
)
echo [✓] Jupyter kernel installed.
echo.

echo [5/5] Setup complete!
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

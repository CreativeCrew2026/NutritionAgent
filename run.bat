@echo off
title NutriGuide AI — IBM Granite Nutrition Agent
color 0A

echo.
echo  ======================================================
echo     NutriGuide AI — IBM Granite Nutrition Agent
echo     Powered by IBM watsonx.ai ^| Flask ^| Python
echo  ======================================================
echo.

:: ─── Check Python ───────────────────────────────────────────
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please install Python 3.10+ from https://python.org
    echo  Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
python --version
echo  [OK] Python found.
echo.

:: ─── Check/create virtual environment ───────────────────────
echo [2/5] Setting up virtual environment...
if not exist "venv\" (
    echo  Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo  [OK] Virtual environment created.
) else (
    echo  [OK] Virtual environment already exists.
)
echo.

:: ─── Activate venv ───────────────────────────────────────────
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo  [OK] Virtual environment activated.
echo.

:: ─── Install dependencies ────────────────────────────────────
echo [4/5] Installing dependencies (this may take a moment)...
pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo  [WARN] Some packages may have failed. Trying again with verbose output...
    pip install -r requirements.txt
)
echo  [OK] Dependencies installed.
echo.

:: ─── Check .env file ─────────────────────────────────────────
echo [5/5] Checking configuration...
if not exist ".env" (
    echo  [INFO] .env file not found.
    echo  Copying .env.example to .env (Demo mode will be used).
    copy .env.example .env >nul
    echo.
    echo  ┌─────────────────────────────────────────────────────┐
    echo  │  OPTIONAL: Configure IBM watsonx.ai credentials     │
    echo  │  Edit .env and add your:                            │
    echo  │    WATSONX_API_KEY  = your IBM Cloud API key        │
    echo  │    WATSONX_PROJECT_ID = your watsonx project ID     │
    echo  │  Get credentials: https://cloud.ibm.com/            │
    echo  │                                                     │
    echo  │  Without credentials, the app runs in Demo Mode.   │
    echo  └─────────────────────────────────────────────────────┘
    echo.
) else (
    echo  [OK] .env configuration found.
)
echo.

:: ─── Create plans directory ──────────────────────────────────
if not exist "nutrition_plans\" (
    mkdir nutrition_plans
    echo  [OK] nutrition_plans directory created.
)

:: ─── Launch server ────────────────────────────────────────────
echo  ======================================================
echo    Starting NutriGuide AI Server...
echo    Open your browser at: http://localhost:5000
echo    Press Ctrl+C to stop the server.
echo  ======================================================
echo.

:: Auto-open browser after 3 seconds
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

:: Start Flask app
python app.py

echo.
echo  Server stopped.
pause

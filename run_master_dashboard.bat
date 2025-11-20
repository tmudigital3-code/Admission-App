@echo off
echo Admission Analytics Suite - Master Dashboard
echo ============================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not available
    pause
    exit /b 1
)

REM Install or upgrade required packages
echo Installing/upgrading required packages...
pip install -r requirements.txt

REM Check if installation was successful
if %errorlevel% neq 0 (
    echo Error: Failed to install required packages
    pause
    exit /b 1
)

REM Run the Streamlit app
echo Starting the Admission Analytics Suite...
streamlit run master_dashboard.py

pause
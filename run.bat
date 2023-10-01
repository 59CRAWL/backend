@echo off

REM Step 1: Create a virtual environment (venv)
python -m venv venv

REM Step 2: Activate the virtual environment
call venv\Scripts\activate

REM Step 3: Install required Python packages
pip install -r requirements.txt

REM Step 3: Move to app directory
cd /d app

REM Step 4: Run your Flask application
start cmd /k "python app.py"

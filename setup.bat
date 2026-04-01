@echo off
echo 🔧 Setting up project on Windows...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

echo ✅ Setup complete! Virtual environment is ready.
pause

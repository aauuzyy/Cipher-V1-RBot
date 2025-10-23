@echo off
title Cipher V1 RBot Setup
echo ========================================
echo       CIPHER V1 RBOT SETUP
echo ========================================
echo.
echo This script will set up your Roblox bot environment.
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.
echo Creating virtual environment...
if exist ".venv" (
    echo Virtual environment already exists.
) else (
    python -m venv .venv
    echo Virtual environment created!
)

echo.
echo Installing dependencies...
.venv\Scripts\pip install -r requirements.txt

echo.
echo ========================================
echo         SETUP COMPLETE!
echo ========================================
echo.
echo To run the bot:
echo 1. Double-click 'launch_bot.bat'
echo 2. Or run: python cipher_bot.py
echo.
echo Happy botting!
pause
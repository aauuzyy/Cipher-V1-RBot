@echo off
title Cipher V1 RBot Launcher
echo ========================================
echo       CIPHER V1 RBOT LAUNCHER
echo ========================================
echo.
echo Checking Python environment...
if not exist ".venv\Scripts\python.exe" (
    echo Error: Python virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then run: .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Python environment found!
echo.
echo Instructions:
echo 1. Make sure Roblox is running and you're in a game
echo 2. Position your character in an open area
echo 3. The bot system will initialize first
echo 4. Use F1 to START the bot behavior
echo 5. Use F2 to STOP the bot behavior
echo 6. Press Ctrl+C to exit completely
echo.
echo Press any key to launch the bot system...
pause > nul

echo.
echo Starting Cipher Bot System...
.venv\Scripts\python.exe cipher_bot.py

echo.
echo Bot system has stopped.
pause
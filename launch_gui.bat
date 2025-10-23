@echo off
title Cipher V1 RBot - Professional GUI Launcher
echo ========================================
echo       CIPHER V1 RBOT GUI LAUNCHER
echo ========================================
echo.
echo Checking Python environment...
if not exist ".venv\Scripts\python.exe" (
    echo Error: Python virtual environment not found!
    echo Please run setup.bat first!
    pause
    exit /b 1
)

echo Python environment found!
echo.
echo Starting Cipher V1 RBot Professional Interface...
echo.

.venv\Scripts\python.exe cipher_gui.py

echo.
echo GUI has closed.
pause
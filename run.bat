@echo off
title Perkenalan Diri Interaktif - Reziao Rajendra Dianta
echo ========================================================
echo   Menjalankan Program Deteksi Gestur Tangan & Suara
echo ========================================================
echo.
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Terjadi kesalahan saat menjalankan program.
    pause
)

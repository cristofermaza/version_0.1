cat > iniciar.bat <<'EOF'
@echo off
title SIGEP - Sistema de Gestion de Personal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Ejecuta primero instalar.bat
    pause
    exit /b 1
)

".venv\Scripts\python.exe" app.py

if errorlevel 1 (
    echo SIGEP termino con un error.
    pause
)
EOF

cat > instalar.bat <<'EOF'
@echo off
title Instalador de SIGEP
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado.
    echo Instala Python desde https://www.python.org/downloads/
    echo Marca la opcion Add Python to PATH.
    pause
    exit /b 1
)

echo [1/3] Creando entorno virtual...
if not exist ".venv\Scripts\python.exe" (
    py -m venv .venv
    if errorlevel 1 goto error
)

echo [2/3] Actualizando pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto error

echo [3/3] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo Instalacion completada.
pause
exit /b 0

:error
echo ERROR: Fallo la instalacion.
pause
exit /b 1
EOF
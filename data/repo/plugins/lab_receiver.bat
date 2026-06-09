@echo off
TITLE SysAva Lab Receiver
SETLOCAL EnableDelayedExpansion

:: Garante que o script rode no diretorio onde ele esta localizado
cd /d "%~dp0"

echo =======================================================
echo         SysAva - Receptor de Monitoramento
echo =======================================================

:: 1. Localizacao do interpretador Python (Tenta o venv do SysAva primeiro)
set "PYTHON_CMD=python"
if exist "..\..\..\.sysenv\Scripts\python.exe" (
    set "PYTHON_CMD=..\..\..\.sysenv\Scripts\python.exe"
    echo [INFO] Usando ambiente virtual detectado em .sysenv
) else (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERRO] Python nao encontrado no PATH nem no ambiente virtual.
        pause
        exit /b
    )
    echo [AVISO] Ambiente virtual nao encontrado. Usando Python global.
)

:: 2. Garante que as dependencias estao instaladas
echo [INFO] Verificando dependencias (flask)...
"%PYTHON_CMD%" -m pip install flask >nul 2>&1
if %errorlevel% neq 0 echo [AVISO] Falha ao verificar/instalar Flask. O receptor pode falhar.

:: 2. Loop de Auto-Recuperacao (Watchdog)
:RESTART
echo [%TIME%] Verificando disponibilidade da porta 5000...
netstat -ano | findstr :5000 | findstr LISTENING > nul
if %errorlevel% equ 0 (
    echo [AVISO] A porta 5000 ja esta ocupada. O receptor pode ja estar rodando.
    timeout /t 15
    goto RESTART
)

echo [%TIME%] Iniciando Receptor SysAva...
"%PYTHON_CMD%" lab_receiver.py
echo [ALERTA] O receptor encerrou inesperadamente. Reiniciando em 5 segundos...
timeout /t 5
goto RESTART
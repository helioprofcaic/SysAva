@echo off
TITLE SysAva Lab Receiver
SETLOCAL EnableDelayedExpansion

:: Garante que o script rode no diretorio onde ele esta localizado
cd /d "%~dp0"

echo =======================================================
echo         SysAva - Receptor de Monitoramento v2
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
        exit /b 1
    )
    echo [AVISO] Ambiente virtual nao encontrado. Usando Python global.
)

:: 2. Garante que as dependencias estao instaladas (Flask)
echo [INFO] Verificando dependencias (flask, waitress, google-generativeai)...
call "%PYTHON_CMD%" -m pip install flask waitress google-generativeai >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Falha ao verificar/instalar Flask. O receptor pode falhar.
)

:: 3. Verificação e Configuração do Firewall
echo [INFO] Verificando regra de Firewall para a porta 5000...
netsh advfirewall firewall show rule name="SysAva Lab Receiver (TCP 5000)" >nul
if %errorlevel% == 0 (
    echo [OK] Regra de firewall ja existe.
) else (
    echo [AVISO] Regra de firewall nao encontrada. Tentando criar...
    
    rem Resolve o caminho para absoluto para o netsh
    netsh advfirewall firewall add rule name="SysAva Lab Receiver (TCP 5000)" dir=in action=allow protocol=TCP localport=5000 profile=any >nul 2>&1
    
    if !errorlevel! neq 0 (
        echo [!] Falha ao criar regra. Solicitando permissao de Administrador...
        powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs" >nul 2>&1
        echo [i] Se a janela do Administrador aparecer, clique em 'Sim'. O script sera reiniciado.
        exit /b
    ) else (
        echo [OK] Regra de firewall criada com sucesso.
    )
)

:: Loop de Auto-Recuperacao (Watchdog)
:RESTART
echo [%TIME%] Iniciando Receptor SysAva...
call "%PYTHON_CMD%" lab_receiver.py

echo.
echo [DEBUG] Verificando se o servidor esta escutando na porta 5000...
timeout /t 2 >nul
netstat -ano | findstr ":5000"

echo [ALERTA] O receptor encerrou inesperadamente. Reiniciando em 5 segundos...
timeout /t 5
goto RESTART
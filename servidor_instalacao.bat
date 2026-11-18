@echo off
TITLE SysAva - Servidor de Instalacao (arquivos para os clientes)
SETLOCAL EnableDelayedExpansion
cd /d "%~dp0"

set "PLUGIN_DIR=%~dp0data\repo\plugins\monitor"
if not exist "%PLUGIN_DIR%\lab_receiver.py" set "PLUGIN_DIR=%~dp0data\repo\plugins"
set "RECEIVER=%PLUGIN_DIR%\lab_receiver.py"

echo =========================================================
echo    SysAva - Servidor de Instalacao / Atualizacao
echo    (serve os agentes e utilitarios para as maquinas)
echo =========================================================
echo.

if not exist "%RECEIVER%" (
    echo [ERRO] Nao encontrei "%RECEIVER%".
    pause
    exit /b 1
)

:: 1. Python (venv .sysenv ou global)
set "PYTHON_CMD=%~dp0.sysenv\Scripts\python.exe"
if exist "%PYTHON_CMD%" (
    echo [INFO] Usando o ambiente virtual .sysenv
) else (
    set "PYTHON_CMD=python"
    python --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo [ERRO] Python nao encontrado ^(.sysenv nem no PATH^).
        pause
        exit /b 1
    )
    echo [AVISO] .sysenv nao encontrado; usando o Python global.
)

:: 2. Dependencias
echo [INFO] Verificando dependencias (flask, waitress, filelock)...
call "%PYTHON_CMD%" -m pip install --quiet flask waitress filelock
if !errorlevel! neq 0 echo [AVISO] Falha ao instalar dependencias; o servidor ainda pode funcionar.

:: 3. Firewall (TCP 5000 + UDP 5001) - pede Administrador se necessario
netsh advfirewall firewall show rule name="SysAva Lab Receiver (TCP 5000)" >nul 2>&1
if !errorlevel! neq 0 (
    echo [INFO] Criando regra de firewall TCP 5000 ^(requer Administrador^)...
    netsh advfirewall firewall add rule name="SysAva Lab Receiver (TCP 5000)" dir=in action=allow protocol=TCP localport=5000 profile=any >nul 2>&1
    if !errorlevel! neq 0 (
        echo [!] Sem permissao. Reabrindo como Administrador...
        powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs" >nul 2>&1
        exit /b
    )
)
netsh advfirewall firewall show rule name="SysAva Lab Receiver (UDP 5001)" >nul 2>&1
if !errorlevel! neq 0 (
    netsh advfirewall firewall add rule name="SysAva Lab Receiver (UDP 5001)" dir=in action=allow protocol=UDP localport=5001 profile=any >nul 2>&1
)

:: 4. Descobrir o IP do notebook (interface com gateway padrao)
set "LOCAL_IP="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "(Get-NetIPConfiguration).Where({ $_.IPv4DefaultGateway -ne $null })[0].IPv4Address.IPAddress"`) do set "LOCAL_IP=%%i"
if not defined LOCAL_IP set "LOCAL_IP=<ip-do-notebook>"

echo.
echo =========================================================
echo   Em cada maquina cliente, abra o navegador em:
echo.
echo       http://%LOCAL_IP%:5000/setup
echo.
echo   Diagnostico:  http://%LOCAL_IP%:5000/diagnostics
echo   Maquinas:     http://%LOCAL_IP%:5000/
echo =========================================================
echo.

:: 5. Ja esta rodando?
netstat -ano | findstr ":5000" | findstr "LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo [INFO] O servidor JA esta em execucao na porta 5000.
    echo        Use a URL acima. Nada a fazer.
    echo.
    pause
    exit /b 0
)

:: 6. Loop com auto-recuperacao (watchdog)
:RESTART
echo [%TIME%] Iniciando o servidor de instalacao...
call "%PYTHON_CMD%" "%RECEIVER%"
echo.
echo [ALERTA] O servidor encerrou. Reiniciando em 5 segundos... ^(CTRL+C para sair^)
timeout /t 5 >nul
goto RESTART

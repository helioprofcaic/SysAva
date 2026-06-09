@echo off
:: Define a codificação para UTF-8 para suportar acentos no console
chcp 65001 > nul

set "SCRIPT_PATH=%~dp0data\repo\plugins\lab_agent.ps1"
set "LOG_FILE=%~dp0install_log.txt"

echo ============================================================
echo   SYSAVA - Instalador do Agente (Destino: C:\Local)
echo ============================================================
echo.
echo Iniciando instalação... Por favor, aguarde.
echo O progresso detalhado está sendo gravado em: install_log.txt

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%" > "%LOG_FILE%" 2>&1

echo.
echo [OK] Processo finalizado. Abrindo log para conferência...
start notepad.exe "%LOG_FILE%"
pause
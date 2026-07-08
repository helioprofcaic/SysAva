@echo off
title Diagnóstico SysAva
chcp 65001 > nul

REM Verifica se o ambiente virtual existe
if not exist ".sysenv\Scripts\python.exe" (
    echo [!] Ambiente virtual .sysenv não encontrado. Execute o run.bat primeiro.
    pause
    exit /b
)

echo Verificando dependências (psutil, requests)...
".sysenv\Scripts\python.exe" -m pip install psutil requests --quiet

REM Verifica se o argumento --watch foi passado para o .bat
if /i "%1" == "--watch" (
    echo Rodando check_serv em modo de monitoramento contínuo...
    ".sysenv\Scripts\python.exe" check_serv.py --watch
) else (
    echo Rodando diagnóstico completo do check_serv...
    ".sysenv\Scripts\python.exe" check_serv.py
)

echo.
pause
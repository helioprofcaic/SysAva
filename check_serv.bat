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

echo Rodando check_serv...
".sysenv\Scripts\python.exe" check_serv.py --watch

echo.
pause
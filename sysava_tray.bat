@echo off
title SysAva - Bandeja dos Apps
cd /d "%~dp0"
echo Abrindo o icone do SysAva na bandeja (ao lado do relogio)...
echo.
echo    Clique no icone para: abrir o SysAva, abrir os outros apps,
echo    ver o status dos servidores e marcar "Iniciar com o Windows".
echo.
wscript.exe "%~dp0sysava_tray.vbs"
timeout /t 2 >nul

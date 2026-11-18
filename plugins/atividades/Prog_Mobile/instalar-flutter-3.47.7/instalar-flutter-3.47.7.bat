@echo off
title SysAva - Instalar Flutter 3.47.7
cd /d "%~dp0"
echo Instalando o Flutter 3.47.7 (download/extracao/PATH)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0instalar-flutter-3.47.7.ps1" %*
echo.
pause

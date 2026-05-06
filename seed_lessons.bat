@echo off
chcp 65001 > nul
setlocal
set PYTHONUTF8=1

REM Converte para caminho absoluto do Windows
set "PYTHON_EXECUTABLE=C:\Local\Apps\Python\Python312\python.exe"
set "VENV_DIR=.sysenv"

if not defined VENV_PATH (
  for %%a in ("%CD%\%VENV_DIR%") do set "VENV_PATH=%%~fa"
)


REM Popula o banco de dados com as aulas
echo.
echo Populando o banco de dados com as aulas em lote... 
"%VENV_DIR%\Scripts\python.exe" scripts/seed_lessons.py > data\populated_lessons.log 2>&1
set SEED_EXIT_CODE=%errorlevel%
type data\populated_lessons.log
if %SEED_EXIT_CODE% neq 0 (
    echo AVISO: Houve erros na importacao de aulas. Verifique o log acima.
    pause
)
echo.

pause
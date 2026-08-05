@echo off
chcp 65001 > nul
setlocal
set PYTHONUTF8=1

REM Converte para caminho absoluto do Windows
set "PYTHON_EXECUTABLE=.sysenv\Scripts\python.exe"

REM Popula o banco de dados com as aulas
echo.
echo Populando o banco de dados com as aulas em lote... 
"%PYTHON_EXECUTABLE%" scripts/seed_lessons.py > data\populated_lessons.log 2>&1
set SEED_EXIT_CODE=%errorlevel%
type data\populated_lessons.log
if %SEED_EXIT_CODE% neq 0 (
    echo AVISO: Houve erros na importacao de aulas. Verifique o log acima.
    pause
)
echo.

pause
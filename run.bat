@echo off
chcp 65001 > nul
setlocal
set PYTHONUTF8=1

REM Converte para caminho absoluto do Windows
set "PYTHON_EXECUTABLE=C:\Local\apps\miniconda3\python.exe"
set "VENV_DIR=.sysenv"


if not defined VENV_PATH (
  for %%a in ("%CD%\%VENV_DIR%") do set "VENV_PATH=%%~fa"
)

REM Cria o ambiente virtual usando script Python
if not exist "%VENV_PATH%\Scripts\python.exe" (
    python create_venv.py
)

REM Verifica se o ambiente virtual existe corretamente
if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo Criando ambiente virtual...
    "%PYTHON_EXECUTABLE%" -m venv "%VENV_PATH%"
)

echo Atualizando o Pip...
"%VENV_PATH%\Scripts\python.exe" -m pip install --upgrade pip

REM Instala/Atualiza dependencias
echo Verificando dependencias...
"%VENV_PATH%\Scripts\pip.exe" install --upgrade pip -r requirements.txt 


REM Verifica se o .env existe antes de popular o banco
if not exist ".env" (
    echo.
    echo AVISO: Arquivo .env nao encontrado.
    echo Por favor, renomeie .env.example para .env e preencha com suas credenciais do Supabase.
    echo Os scripts de populacao do banco de dados serao ignorados.
    echo.
    goto start_app
)

REM Popula o banco de dados com a estrutura da escola
echo.
echo Populando o banco de dados com a estrutura da escola (turmas e disciplinas)... 
"%VENV_DIR%\Scripts\python.exe" scripts/seed_data.py
if %errorlevel% neq 0 (
    echo.
    echo FALHA CRITICA ao popular estrutura da escola. Verifique a conexao com o Supabase e se as tabelas foram criadas.
    pause
    exit /b 1
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

:ask_students
echo.

CHOICE /C sn /T 10 /D n /M "Deseja popular o banco com os ALUNOS? A importacao sera ignorada em 10 segundos..."

REM CHOICE define ERRORLEVEL: 1 para 's', 2 para 'n' (ou timeout)
if %errorlevel% == 1 goto seed_students
if %errorlevel% == 2 goto start_app

echo.
goto start_app

set /p seed_choice=Voce deseja popular o banco de dados com os ALUNOS? (s/n): 
if /i "%seed_choice%"=="s" (
    goto seed_students
)
if /i "%seed_choice%"=="n" (
    goto start_app
)
echo Resposta invalida. Por favor, digite 's' para sim ou 'n' para nao.
goto ask_students


:seed_students
REM Popula o banco de dados com os alunos
echo.
echo Populando o banco de dados com os alunos...
"%VENV_DIR%\Scripts\python.exe" scripts/seed_students.py
if %errorlevel% neq 0 (
    echo AVISO: Houve erros na importacao de alunos. Verifique o log acima.
    pause
)
echo.

goto start_app
:start_app
REM Forca o modo local ignorando o secrets.toml
set FORCE_LOCAL_MODE=1

REM Lê o nome da escola do arquivo de configuração para exibir na mensagem
set "SCHOOL_CONFIG_FILE=data\Turmas\Escola.txt"
set school_name=SysAva
if exist "%SCHOOL_CONFIG_FILE%" set /p school_name=<"%SCHOOL_CONFIG_FILE%"

REM Executa a aplicacao
echo.
echo Iniciando o %school_name%...


REM Executa a aplicacao
echo.
echo Iniciando o SysAva CETI Raldir...

call "%VENV_DIR%\Scripts\streamlit.exe" run app.py
pause

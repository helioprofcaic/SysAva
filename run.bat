
@echo off
setlocal

set "VENV_DIR=.venv"

REM Verifica se o Python esta instalado
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao encontrado. Por favor instale o Python.
    pause
    exit /b 1
)

REM Verifica se o ambiente virtual existe
if not exist "%VENV_DIR%" (
    echo Criando ambiente virtual...
    python -m venv "%VENV_DIR%"
)

REM Ativa o ambiente virtual
call "%VENV_DIR%\Scripts\activate"

REM Instala/Atualiza dependencias
echo Verificando dependencias...
pip install -r requirements.txt

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
python scripts/seed_data.py
if %errorlevel% neq 0 (
    echo.
    echo FALHA CRITICA ao popular estrutura da escola. Verifique a conexao com o Supabase e se as tabelas foram criadas.
    pause
    exit /b 1
)

REM Popula o banco de dados com as aulas
echo.
echo Populando o banco de dados com as aulas em lote...
python scripts/seed_lessons.py
if %errorlevel% neq 0 (
    echo AVISO: Houve erros na importacao de aulas. Verifique o log acima.
    pause
)
echo.

:ask_students
echo.
set /p "seed_choice=Voce deseja popular o banco de dados com os ALUNOS? (s/n): "
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
python scripts/seed_students.py
if %errorlevel% neq 0 (
    echo AVISO: Houve erros na importacao de alunos. Verifique o log acima.
    pause
)
echo.

goto start_app

:start_app
REM Forca o modo local ignorando o secrets.toml
set FORCE_LOCAL_MODE=1

REM Executa a aplicacao
echo.
echo Iniciando o SysAva CETI Raldir...
streamlit run app.py
pause

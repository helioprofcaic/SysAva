@echo off
setlocal

REM Garante que o script rode a partir do diretorio onde ele esta salvo
cd /d "%~dp0"

set "VENV_DIR=.venv"

REM Verifica se o Python esta instalado
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao encontrado. Por favor instale o Python.
    pause
    exit /b 1
)

REM Determina o caminho dos scripts do venv (pode ser 'Scripts' ou 'bin')
set "VENV_SCRIPTS_DIR=%VENV_DIR%\Scripts"
if not exist "%VENV_SCRIPTS_DIR%\activate.bat" (
    set "VENV_SCRIPTS_DIR=%VENV_DIR%\bin"
)

REM Se o script de ativacao ainda nao existe, cria o ambiente virtual
if not exist "%VENV_SCRIPTS_DIR%\activate.bat" (
    echo.
    echo Ambiente virtual nao encontrado ou incompleto.
    echo Criando ambiente virtual...
    REM Remove o diretorio antigo se existir para garantir uma instalacao limpa
    if exist "%VENV_DIR%" (
        echo Removendo ambiente antigo...
        rmdir /s /q "%VENV_DIR%"
        if exist "%VENV_DIR%" (
            echo FALHA ao remover o diretorio .venv antigo. Feche quaisquer programas usando-o.
            pause
            exit /b 1
        )
    )
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo.
        echo FALHA ao criar o ambiente virtual. Verifique sua instalacao do Python.
        pause
        exit /b 1
    )
    
    REM Re-determina o caminho dos scripts apos a criacao
    set "VENV_SCRIPTS_DIR=%VENV_DIR%\Scripts"
    if not exist "%VENV_SCRIPTS_DIR%\activate.bat" (
        set "VENV_SCRIPTS_DIR=%VENV_DIR%\bin"
    )

    REM Verificacao final
    if not exist "%VENV_SCRIPTS_DIR%\activate.bat" (
        echo.
        echo FALHA CRITICA: O script de ativacao nao foi encontrado em 'Scripts' ou 'bin' apos a criacao do ambiente.
        pause
        exit /b 1
    )
)

REM Ativa o ambiente virtual
echo.
echo Ativando ambiente virtual...
call "%VENV_SCRIPTS_DIR%\activate.bat"
if %errorlevel% neq 0 (
    echo FALHA ao ativar o ambiente virtual.
    pause
    exit /b 1
)

REM Instala/Atualiza dependencias
echo.
echo Verificando dependencias...
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
if %errorlevel% neq 0 (
    echo FALHA ao instalar dependencias.
    pause
    exit /b 1
)

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

REM Popula o banco de dados com os alunos
echo.
echo Populando o banco de dados com os alunos...
python scripts/seed_students.py
echo.

:start_app
REM Forca o modo local ignorando o secrets.toml
set FORCE_LOCAL_MODE=1

REM Executa a aplicacao
echo.
echo Iniciando o SysAva CETI Raldir...
streamlit run app.py
pause

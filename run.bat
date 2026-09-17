@echo off
chcp 65001 > nul
taskkill /f /im streamlit.exe >nul 2>&1
setlocal EnableDelayedExpansion
set "PYTHONUTF8=1"

REM ==========================================
REM 1. BUSCA AUTOMÁTICA DO PYTHON
REM ==========================================
set "PYTHON_EXECUTABLE="
for /f "tokens=*" %%i in ('py -3.11 -c "import sys; print(sys.executable)" 2^>nul') do (
    set "PYTHON_EXECUTABLE=%%i"
)

if not defined PYTHON_EXECUTABLE (
    echo.
    echo [ERRO CRITICO] Python 3.11 nao foi encontrado no seu sistema.
    echo Esta versao e necessaria para compatibilidade com as bibliotecas de IA.
    echo.
    echo [ACAO] Por favor, instale o Python 3.11 a partir do site oficial: https://www.python.org/downloads/release/python-3119/
    echo Certifique-se de marcar a opcao "Add python.exe to PATH" durante a instalacao.
    pause
    exit /b 1
)

:: Obtém e exibe a versão do Python base encontrado
for /f "usebackq tokens=*" %%v in (`""%PYTHON_EXECUTABLE%" --version"`) do set "SYS_PYTHON_VER=%%v"
echo [OK] Python base (3.11) detectado: "%PYTHON_EXECUTABLE%"

REM ==========================================
REM 2. GERENCIAMENTO DO AMBIENTE VIRTUAL
REM ==========================================
set "VENV_DIR=.sysenv"
if not defined VENV_PATH (
    for %%a in ("%CD%\%VENV_DIR%") do set "VENV_PATH=%%~fa"
)

REM Verifica se o venv existente é compatível com o Python do sistema
if exist "%VENV_PATH%\Scripts\python.exe" (
    for /f "usebackq tokens=*" %%v in (`""%VENV_PATH%\Scripts\python.exe" --version"`) do set "VENV_PYTHON_VER=%%v"
    
    REM Compara as strings de versão. Se forem diferentes, o venv é inválido.
    if "!SYS_PYTHON_VER!" NEQ "!VENV_PYTHON_VER!" (
        echo.
        echo [AVISO] Incompatibilidade de versão detectada!
        echo   - Python do Sistema: !SYS_PYTHON_VER!
        echo   - Python do Venv:    !VENV_PYTHON_VER!
        echo [INFO] Removendo ambiente virtual antigo para recriá-lo...
        rmdir /s /q "%VENV_PATH%"
    )
)

REM Criação padrão via module venv caso o ambiente ainda não exista
if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo Criando ambiente virtual em "%VENV_PATH%"...
    "%PYTHON_EXECUTABLE%" -m venv "%VENV_PATH%"
)

REM ==========================================
REM 3. DIAGNÓSTICO E CONFIRMAÇÃO DO VENV
REM ==========================================
if exist "%VENV_PATH%\Scripts\python.exe" (
    for /f "usebackq tokens=*" %%v in (`""%VENV_PATH%\Scripts\python.exe" --version"`) do set "VENV_PYTHON_VER=%%v"
    echo [OK] Ambiente virtual ativo em "%VENV_PATH%"
    echo [INFO] Versao do Python no VENV: !VENV_PYTHON_VER!
) else (
    echo [ERRO] Falha ao criar ou localizar o ambiente virtual.
    pause & exit /b 1
)

REM ==========================================
REM 4. INSTALAÇÃO DE DEPENDÊNCIAS (OPCIONAL)
REM ==========================================
CHOICE /C sn /T 7 /D n /M "Deseja verificar e atualizar as bibliotecas (requirements.txt)?"
if %errorlevel% == 1 (
    echo [INFO] Atualizando Pip e instalando dependências...
    "%VENV_PATH%\Scripts\python.exe" -m pip install --upgrade pip
    "%VENV_PATH%\Scripts\pip.exe" install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERRO] Falha ao instalar dependências. Verifique sua conexão e o arquivo requirements.txt.
        pause & exit /b 1
    )
)

REM ==========================================
REM 5. INICIALIZAÇÃO DAS APLICAÇÕES
REM ==========================================
echo [INFO] Iniciando API de gerenciamento de modelos em segundo plano...
start "Model Manager API" /B "%VENV_PATH%\Scripts\python.exe" scripts/model_manager_api.py

REM Força o Streamlit a escutar em todas as interfaces de rede
set STREAMLIT_SERVER_ADDRESS=0.0.0.0

REM Força o modo local ignorando o secrets.toml
set FORCE_LOCAL_MODE=1

REM Lê o nome da escola do arquivo de configuração para exibir na mensagem
set "SCHOOL_CONFIG_FILE=data\Turmas\Escola.txt"
set school_name=SysAva
if exist "%SCHOOL_CONFIG_FILE%" set /p school_name=<"%SCHOOL_CONFIG_FILE%"

:menu
cls
echo ========================================================
echo                 PAINEL DE CONTROLE SYSAVA               
echo ========================================================
echo.
echo Selecione a aplicação que deseja iniciar:
echo.
echo [1] Iniciar o %school_name% (Aplicação Principal)
echo [2] Iniciar o Verificador de Duplicatas (historico_aulas)
echo [3] Iniciar o Monitor de Consumo do Supabase (Egress)
echo [4] Iniciar o Acompanhamento de Planejamento e Registro
echo [5] Sair do Painel
echo.
echo ========================================================
set /p escolha="Digite a opção desejada (1-5): "

if "%escolha%"=="1" goto start_app
if "%escolha%"=="2" goto start_dup
if "%escolha%"=="3" goto start_mon
if "%escolha%"=="4" goto start_plan
if "%escolha%"=="5" exit /b 0
goto menu

:start_app
echo.
echo Iniciando o %school_name%...
call "%VENV_PATH%\Scripts\streamlit.exe" run app.py
pause
goto menu

:start_dup
echo.
echo Iniciando o Verificador de Duplicatas...
call "%VENV_PATH%\Scripts\streamlit.exe" run apps/duplicate_checker/duplicate_checker_streamlit.py
pause
goto menu

:start_mon
echo.
echo Iniciando o Monitor de Consumo Supabase...
call "%VENV_PATH%\Scripts\streamlit.exe" run apps/supabase_monitor/supabase_monitor_streamlit.py
pause
goto menu

:start_plan
echo.
echo Iniciando o Acompanhamento de Planejamento e Registro (porta 8510)...
call "%VENV_PATH%\Scripts\streamlit.exe" run apps/planejamento_registro/planejamento_registro_streamlit.py --server.port 8510
pause
goto menu

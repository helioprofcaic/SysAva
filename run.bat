@echo off
chcp 65001 > nul
taskkill /f /im streamlit.exe >nul 2>&1
setlocal enabledelayedexpansion
set "PYTHONUTF8=1"

REM ==========================================
REM 1. BUSCA AUTOMÁTICA DO PYTHON
REM ==========================================
set "PYTHON_EXECUTABLE="

:: Prioridade 1: Usar o launcher do Windows (py.exe), que é mais confiável
if not defined PYTHON_EXECUTABLE (
    for /f "tokens=*" %%i in ('py -c "import sys; print(sys.executable)" 2^>nul') do (
        set "PYTHON_EXECUTABLE=%%i"
    )
)

:: Prioridade 2: Tenta localizar o python no PATH do sistema se o py.exe falhar
if not defined PYTHON_EXECUTABLE (
    for /f "delims=" %%i in ('where python 2^>nul') do (
        if not defined PYTHON_EXECUTABLE set "PYTHON_EXECUTABLE=%%i"
    )
)

:: Fallback: Tenta o caminho fixo do Miniconda caso nada acima funcione
if not defined PYTHON_EXECUTABLE (
    if exist "C:\Local\apps\miniconda3\python.exe" (
        set "PYTHON_EXECUTABLE=C:\Local\apps\miniconda3\python.exe"
    )
)

:: Se mesmo assim não encontrar nada, exibe erro e encerra
if not defined PYTHON_EXECUTABLE (
    echo [ERRO] Nenhuma instalação do Python foi encontrada no sistema.
    pause
    exit /b 1
)

:: Obtém e exibe a versão do Python base encontrado
for /f "tokens=*" %%v in ('"%PYTHON_EXECUTABLE%" --version 2^>1') do set "SYS_PYTHON_VER=%%v"
echo [OK] Python base detectado: "%PYTHON_EXECUTABLE%" (%SYS_PYTHON_VER%)

REM ==========================================
REM 2. GERENCIAMENTO DO AMBIENTE VIRTUAL
REM ==========================================
set "VENV_DIR=.sysenv"

if not defined VENV_PATH (
    for %%a in ("%CD%\%VENV_DIR%") do set "VENV_PATH=%%~fa"
)

REM Verifica se o venv existente é compatível com o Python do sistema
if exist "%VENV_PATH%\Scripts\python.exe" (
    for /f "tokens=*" %%v in ('"%VENV_PATH%\Scripts\python.exe" --version 2^>1') do set "VENV_PYTHON_VER=%%v"
    
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

REM Cria o ambiente virtual usando script Python customizado (se existir)
if not exist "%VENV_PATH%\Scripts\python.exe" (
    if exist "create_venv.py" (
        "%PYTHON_EXECUTABLE%" create_venv.py
    )
)

REM Criação padrão via module venv caso o ambiente ainda não exista
if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo Criando ambiente virtual em "%VENV_PATH%"...
    "%PYTHON_EXECUTABLE%" -m venv "%VENV_PATH%"
)

REM Fallback para 'virtualenv' se 'venv' falhou (comum em Python embeddable)
if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo [AVISO] O modulo 'venv' nao foi encontrado. Tentando usar 'virtualenv' como alternativa.
    echo [INFO] Instalando 'virtualenv'...
    "%PYTHON_EXECUTABLE%" -m pip install virtualenv
    if !errorlevel! neq 0 (
        echo [ERRO] Falha ao instalar o pacote 'virtualenv'. Verifique a conexao com a internet.
        pause & exit /b 1
    )
    "%PYTHON_EXECUTABLE%" -m virtualenv "%VENV_PATH%"
)
REM ==========================================
REM 3. DIAGNÓSTICO E CONFIRMAÇÃO DO VENV
REM ==========================================
if exist "%VENV_PATH%\Scripts\python.exe" (
    for /f "tokens=*" %%v in ('"%VENV_PATH%\Scripts\python.exe" --version 2^>1') do set "VENV_PYTHON_VER=%%v"
    echo [OK] Ambiente virtual ativo em "%VENV_PATH%"
    echo [INFO] Versao do Python no VENV: !VENV_PYTHON_VER!
) else (
    echo [ERRO] Falha ao criar ou localizar o ambiente virtual.
    pause
    exit /b 1
)

echo Atualizando o Pip...
"%VENV_PATH%\Scripts\python.exe" -m pip install --upgrade pip

echo.
echo Garantindo compatibilidade do Streamlit com Starlette...
"%VENV_PATH%\Scripts\pip.exe" install --upgrade "streamlit" "starlette<0.37"

REM Instala/Atualiza dependencias
echo Verificando dependencias...
"%VENV_PATH%\Scripts\pip.exe" install --upgrade -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo FALHA CRITICA ao instalar dependencias. Verifique se nao ha outro processo do SysAva/Streamlit em execucao.
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

:check_network
echo.
echo Verificando status da rede...
set "NETWORK_STATUS=Offline"
for /f "tokens=3,*" %%a in ('netsh wlan show interfaces ^| find "Estado"') do (
    if "%%a"=="conectado" set "NETWORK_STATUS=Online"
)

if "!NETWORK_STATUS!"=="Offline" (
    echo.
    echo AVISO: Nenhuma conexao Wi-Fi ativa detectada.
    CHOICE /C sn /T 10 /D n /M "Deseja tentar criar um Hotspot Movel local (Rede: SysAva-Offline)? Ignorando em 10s..."
    if !errorlevel! == 1 (
        echo.
        echo Configurando e iniciando Hotspot Movel...
        netsh wlan set hostednetwork mode=allow ssid=SysAva-Offline key=12345678 >nul
        netsh wlan start hostednetwork
        if !errorlevel! neq 0 (
            echo [ERRO] Falha ao iniciar o hotspot. Execute o 'run.bat' como Administrador.
        ) else (
            echo [OK] Hotspot 'SysAva-Offline' iniciado. Senha: 12345678
            echo Os alunos devem se conectar a esta rede Wi-Fi.
            echo O endereco de acesso sera exibido ao iniciar o sistema.
        )
        echo.
        pause
    )
)

REM Força o Streamlit a escutar em todas as interfaces de rede
set STREAMLIT_SERVER_ADDRESS=0.0.0.0

REM Força o modo local ignorando o secrets.toml
set FORCE_LOCAL_MODE=1

:ask_seed_data
echo.
CHOICE /C sn /T 10 /D n /M "Deseja conferir e atualizar a ESTRUTURA da escola (turmas/disciplinas)? Ignorando em 10s..."
if %errorlevel% == 2 goto skip_seed_data

REM Popula o banco de dados com a estrutura da escola
echo Populando a estrutura da escola... 
"%VENV_PATH%\Scripts\python.exe" scripts/seed_data.py
if %errorlevel% neq 0 (
    echo.
    echo FALHA CRITICA ao popular estrutura da escola. Verifique a conexao com o Supabase e se as tabelas foram criadas.
    pause
    exit /b 1
)
:skip_seed_data

REM Popula a grade horaria
echo Populando a grade horária semanal no banco de dados...
REM Executa o script com o python do ambiente virtual
"%VENV_PATH%\Scripts\python.exe" scripts/seed_grade.py

REM Popula o banco de dados com as aulas
echo.
echo Populando o banco de dados com as aulas em lote... 
REM Chama o script de lote, passando o caminho do python do venv como argumento
call seed_lessons.bat
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
"%VENV_PATH%\Scripts\python.exe" scripts/seed_students.py
if %errorlevel% neq 0 (
    echo AVISO: Houve erros na importacao de alunos. Verifique o log acima.
    pause
)
echo.

goto start_app
:start_app
REM Lê o nome da escola do arquivo de configuração para exibir na mensagem
set "SCHOOL_CONFIG_FILE=data\Turmas\Escola.txt"
set school_name=SysAva
if exist "%SCHOOL_CONFIG_FILE%" set /p school_name=<"%SCHOOL_CONFIG_FILE%"

REM Executa a aplicacao
echo.
echo Iniciando o %school_name%...
call "%VENV_PATH%\Scripts\streamlit.exe" run app.py
pause

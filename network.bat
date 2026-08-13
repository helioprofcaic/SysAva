@echo off
chcp 65001 > nul

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

pause

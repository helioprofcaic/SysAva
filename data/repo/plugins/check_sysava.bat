@echo off
echo ========================================
echo     Status do Agente SysAva (Client)
echo ========================================
echo.

echo [INFO] Identificacao da Rede:
powershell -NoProfile -Command "$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike '*Loopback*' }).IPAddress; Write-Host 'IP Local:' $ip -ForegroundColor Cyan"
echo.

echo [INFO] Verificando Processo:
powershell -NoProfile -Command "$proc = Get-Process -Name 'python' -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*agent*' }; if ($proc) { Write-Host '[OK] O Agente SysAva ESTA RODANDO!' -ForegroundColor Green } else { Write-Host '[ERRO] O Agente SysAva (processo python c/ agent) NAO foi detectado.' -ForegroundColor Red }"

echo.
echo [INFO] Teste de Conexao com o Gateway (192.168.10.1):
powershell -NoProfile -Command "if (Test-Connection -ComputerName 192.168.10.1 -Count 1 -Quiet) { Write-Host '[OK] Gateway alcancavel.' -ForegroundColor Green } else { Write-Host '[FALHA] Gateway (192.168.10.1) nao responde. Verifique a rede!' -ForegroundColor Red }"

echo.
echo --- Ultimos 5 registros do Log ---
powershell -NoProfile -Command "if (Test-Path 'C:\Local\SysVa_lab\agent_runtime.log') { Get-Content 'C:\Local\SysVa_lab\agent_runtime.log' -Tail 5 } else { Write-Host 'Log ainda nao gerado.' -ForegroundColor Yellow }"
echo.
pause

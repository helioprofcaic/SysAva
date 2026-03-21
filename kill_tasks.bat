@echo off
echo Encerrando processos do Python e Streamlit...

REM Força o encerramento de todos os processos python.exe
taskkill /F /IM python.exe /T

echo.
echo Processos encerrados. 
echo IMPORTANTE: Verifique o LM Studio e clique em "Eject" no modelo para liberar o restante da RAM.
pause
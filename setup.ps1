<#
.SYNOPSIS
    Builds a standalone executable for the SysAva application.

.DESCRIPTION
    This script automates the process of creating a standalone executable folder for the
    SysAva Streamlit application using PyInstaller. It performs the following steps:
    1. Sets the script's directory as the current location.
    2. Ensures a Python virtual environment exists and is up-to-date.
    3. Installs all required dependencies, including PyInstaller.
    4. Runs PyInstaller with the necessary arguments to bundle the app,
       including data files, services, and views.
    5. Provides instructions for running the final executable.

.NOTES
    Execution Policy: You may need to set the PowerShell execution policy to run this script.
    Run the following command in an administrative PowerShell window:
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
#>

# Garante que o script pare em caso de erro
$ErrorActionPreference = "Stop"

# Garante que o script rode a partir do diretorio onde ele esta salvo
try {
    Set-Location -Path $PSScriptRoot -ErrorAction Stop
    Write-Host "Diretório de trabalho: $(Get-Location)"
}
catch {
    Write-Error "Não foi possível mudar para o diretório do script. Saindo."
    exit 1
}

$venvDir = ".\.sysenv"

# Verifica se o ambiente virtual existe e cria se necessario
if (-not (Test-Path -Path "$venvDir\Scripts\Activate.ps1")) {
    Write-Host "Ambiente virtual não encontrado. Criando..."
    python -m venv $venvDir
}

# Define os caminhos para os executáveis do ambiente virtual
$pythonExe = "$venvDir\Scripts\python.exe"
$pipExe = "$venvDir\Scripts\pip.exe"

# Instala/Atualiza dependências, incluindo PyInstaller
Write-Host "Instalando/Atualizando dependências..."
& $pipExe install --upgrade pip
& $pipExe install -r requirements.txt

# Executa o PyInstaller
Write-Host "Iniciando o processo de build com PyInstaller. Isso pode levar alguns minutos..."

& "$venvDir\Scripts\pyinstaller.exe" --name "SysAva" --noconfirm --clean `
    --add-data "views;views" `
    --add-data "services;services" `
    --add-data "data;data" `
    app.py

Write-Host "`n"
Write-Host "--------------------------------------------------" -ForegroundColor Green
Write-Host "  Build concluído com sucesso!                    " -ForegroundColor Green
Write-Host "--------------------------------------------------" -ForegroundColor Green
Write-Host "O executável está em: '.\dist\SysAva\'"
Write-Host "Para executar, você precisará copiar os seguintes arquivos para a pasta '.\dist\SysAva\':"
Write-Host "  - O arquivo '.env' (com as credenciais do Supabase)."
Write-Host "  - A pasta '.streamlit' (contendo o arquivo 'secrets.toml')."
Write-Host "`n"
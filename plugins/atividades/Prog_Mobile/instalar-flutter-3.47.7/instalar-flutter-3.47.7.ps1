<#
.SYNOPSIS
    Instala o Flutter 3.47.7 stable no Windows e adiciona ao PATH do usuario.

.DESCRIPTION
    Baixa o zip oficial (se ainda nao existir), extrai para C:\src,
    resultando em C:\src\flutter\bin, e inclui essa pasta no PATH do usuario.
    Se C:\src nao puder ser criado, usa %USERPROFILE%\src.
    Nao instala Android Studio, emulador, JDK nem Android SDK.

.PARAMETER Zip
    Caminho do flutter_windows_3.47.7-stable.zip.

.PARAMETER Destino
    Pasta onde o zip sera extraido (padrao: C:\src).
#>
[CmdletBinding()]
param(
    [string]$Zip = (Join-Path $env:USERPROFILE "Downloads\flutter_windows_3.47.7-stable.zip"),
    [string]$Destino = "C:\src"
)

$ErrorActionPreference = "Stop"
$Url = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.47.7-stable.zip"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[AVISO] Git nao encontrado no PATH. O Flutter precisa do Git para versao/upgrade." -ForegroundColor Yellow
    Write-Host "        Instale com: winget install --id Git.Git -e" -ForegroundColor Yellow
}

if (-not (Test-Path -LiteralPath $Zip)) {
    Write-Host "[INFO] Zip nao encontrado. Baixando de $Url ..." -ForegroundColor Cyan
    try {
        $pastaZip = Split-Path -Parent $Zip
        if ($pastaZip) { New-Item -ItemType Directory -Path $pastaZip -Force | Out-Null }
        Invoke-WebRequest -Uri $Url -OutFile $Zip
    } catch {
        Write-Host "[ERRO] Falha ao baixar o zip: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Baixe manualmente: $Url"
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

try {
    New-Item -ItemType Directory -Path $Destino -Force -ErrorAction Stop | Out-Null
} catch {
    $Destino = Join-Path $env:USERPROFILE "src"
    New-Item -ItemType Directory -Path $Destino -Force | Out-Null
    Write-Host "[AVISO] Sem permissao em C:\src; usando $Destino" -ForegroundColor Yellow
}

Write-Host "[INFO] Extraindo $Zip para $Destino ..." -ForegroundColor Cyan
Expand-Archive -LiteralPath $Zip -DestinationPath $Destino -Force

$flutter = Join-Path $Destino "flutter"
$bin = Join-Path $flutter "bin"

# Se o zip foi extraido um nivel a mais (ex.: C:\src\flutter\flutter), corrige.
if (-not (Test-Path -LiteralPath (Join-Path $bin "flutter.bat"))) {
    $interna = Join-Path $flutter "flutter"
    if (Test-Path -LiteralPath (Join-Path $interna "bin\flutter.bat")) {
        Get-ChildItem -LiteralPath $interna -Force | Move-Item -Destination $flutter -Force
        Remove-Item -LiteralPath $interna -Recurse -Force
    }
}

$flutterBat = Join-Path $bin "flutter.bat"
if (-not (Test-Path -LiteralPath $flutterBat)) {
    Write-Host "[ERRO] Nao encontrei $flutterBat" -ForegroundColor Red
    Write-Host "Confira se o zip foi extraido corretamente."
    Read-Host "Pressione Enter para sair"
    exit 1
}

$pathUsuario = [Environment]::GetEnvironmentVariable("Path", "User")
$partes = ($pathUsuario -split ';') | Where-Object { $_ -and ($_ -ne $bin) }
[Environment]::SetEnvironmentVariable("Path", "$bin;" + ($partes -join ';'), "User")
Write-Host "[OK] PATH do usuario atualizado (na frente): $bin" -ForegroundColor Green

# Atualiza o PATH somente nesta sessao para testar agora.
$env:Path = "$bin;" + (($env:Path -split ';' | Where-Object { $_ -and ($_ -ne $bin) }) -join ';')

Write-Host ""
Write-Host "[INFO] Testando a instalacao..." -ForegroundColor Cyan
& $flutterBat --version

Write-Host ""
Write-Host "Pronto. Abra um terminal NOVO e rode:" -ForegroundColor Cyan
Write-Host "  flutter doctor" -ForegroundColor White
Write-Host "  flutter create meu_app" -ForegroundColor White
Write-Host "  cd meu_app" -ForegroundColor White
Write-Host "  flutter test" -ForegroundColor White
Write-Host ""
Write-Host "Avisos de Android/Visual Studio no flutter doctor sao normais neste guia." -ForegroundColor Gray
Read-Host "Pressione Enter para sair"

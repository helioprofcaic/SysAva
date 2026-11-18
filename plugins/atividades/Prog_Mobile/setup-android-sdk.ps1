<#
.SYNOPSIS
    Instala somente as Android SDK Tools (Command-line Tools) + componentes e AVD,
    sem instalar o Android Studio completo. Configura o Flutter para usar o SDK.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\setup-android-sdk.ps1
    powershell -ExecutionPolicy Bypass -File .\setup-android-sdk.ps1 -ApiLevel 35 -Launch
#>
[CmdletBinding()]
param(
    [int]$ApiLevel = 34,
    [string]$SystemImageTag = "google_apis",
    [string]$AvdName = "pixel_6_api_33",
    [string]$AvdDevice = "pixel_6",
    [switch]$Launch
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    [ok] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "    [!] $msg"  -ForegroundColor Yellow }

# ---------------------------------------------------------------- 1. Java
function Get-JavaHome {
    foreach ($scope in "Machine", "User") {
        $jh = [Environment]::GetEnvironmentVariable("JAVA_HOME", $scope)
        if ($jh -and (Test-Path (Join-Path $jh "bin\java.exe"))) { return $jh }
    }
    foreach ($root in @(
        "C:\Program Files\Eclipse Adoptium",
        "C:\Program Files\Java",
        "C:\Program Files\Microsoft",
        "C:\Program Files\Zulu",
        "C:\Program Files\Android\Android Studio\jbr"
    )) {
        if (Test-Path $root) {
            $cand = Get-ChildItem $root -Directory -ErrorAction SilentlyContinue |
                Where-Object { Test-Path (Join-Path $_.FullName "bin\java.exe") } |
                Sort-Object Name -Descending | Select-Object -First 1
            if ($cand) { return $cand.FullName }
        }
    }
    $java = Get-Command java -ErrorAction SilentlyContinue
    if ($java) { return (Split-Path (Split-Path $java.Source -Parent) -Parent) }
    return $null
}

Write-Step "Verificando JDK"
$JavaHome = Get-JavaHome
if (-not $JavaHome) {
    Write-Warn "JDK nao encontrado. Instalando Temurin 17 via winget..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        & cmd /c "winget install EclipseAdoptium.Temurin.17.JDK -e --accept-package-agreements --accept-source-agreements 2>&1" | Out-Host
    } else {
        throw "JDK nao encontrado e winget indisponivel. Instale o JDK 17+ em https://adoptium.net e rode novamente."
    }
    $JavaHome = Get-JavaHome
    if (-not $JavaHome) { throw "Nao foi possivel detectar o JAVA_HOME. Defina JAVA_HOME manualmente e rode novamente." }
}
$env:JAVA_HOME = $JavaHome
$env:PATH = "$JavaHome\bin;$env:PATH"
Write-Ok "JAVA_HOME = $JavaHome"
$ver = (& cmd /c "`"$JavaHome\bin\java.exe`" -version 2>&1" | Out-String).Trim()
if ($ver) { Write-Ok ($ver -split "`r?`n")[0] }

# ---------------------------------------------------------------- 2. Local do SDK
function Get-SdkPath {
    foreach ($scope in "User", "Machine") {
        $s = [Environment]::GetEnvironmentVariable("ANDROID_HOME", $scope)
        if ($s -and (Test-Path $s)) { return $s }
    }
    foreach ($c in @("$env:LOCALAPPDATA\Android\Sdk", "$env:USERPROFILE\AppData\Local\Android\Sdk", "C:\Android\Sdk")) {
        if (Test-Path $c) { return $c }
    }
    return "$env:LOCALAPPDATA\Android\Sdk"
}

Write-Step "Definindo local do SDK"
$Sdk = Get-SdkPath
New-Item -ItemType Directory -Path (Join-Path $Sdk "cmdline-tools\latest") -Force | Out-Null
$env:ANDROID_HOME = $Sdk
$env:ANDROID_SDK_ROOT = $Sdk
Write-Ok "ANDROID_HOME = $Sdk"

# ---------------------------------------------------------------- 3. Command-line Tools
$SdkManager = Join-Path $Sdk "cmdline-tools\latest\bin\sdkmanager.bat"
$AvdManager = Join-Path $Sdk "cmdline-tools\latest\bin\avdmanager.bat"

if (-not (Test-Path $SdkManager)) {
    Write-Step "Baixando as Android SDK Tools (Command-line Tools)"

    $build = $null
    try {
        $xml = (Invoke-WebRequest -Uri "https://dl.google.com/android/repository/repository2-3.xml" -UseBasicParsing -TimeoutSec 60).Content
        if ($xml -match 'commandlinetools-win-(\d+)_latest\.zip') { $build = $Matches[1] }
    } catch {
        Write-Warn "Nao foi possivel consultar o repositorio do Google; usando build conhecido."
    }
    if (-not $build) { $build = "11076708" }

    $zip = Join-Path $env:TEMP "cmdline-tools.zip"
    $url = "https://dl.google.com/android/repository/commandlinetools-win-$build`_latest.zip"
    Write-Ok "Baixando $url"
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing

    $tmp = Join-Path $env:TEMP "cmdt"
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
    Expand-Archive -Path $zip -DestinationPath $tmp -Force
    Copy-Item (Join-Path $tmp "cmdline-tools\*") (Join-Path $Sdk "cmdline-tools\latest\") -Recurse -Force
    Remove-Item $tmp, $zip -Recurse -Force -ErrorAction SilentlyContinue

    if (-not (Test-Path $SdkManager)) { throw "sdkmanager.bat nao encontrado em $SdkManager" }
    Write-Ok "Command-line Tools instaladas"
} else {
    Write-Step "Command-line Tools ja instaladas"
}
Write-Ok $SdkManager

# ---------------------------------------------------------------- 4. Variaveis de ambiente
Write-Step "Registrando variaveis de ambiente"
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $Sdk, "User")
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", $Sdk, "User")
if (-not [Environment]::GetEnvironmentVariable("JAVA_HOME", "User")) {
    [Environment]::SetEnvironmentVariable("JAVA_HOME", $JavaHome, "User")
}

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$add = @(
    (Join-Path $Sdk "cmdline-tools\latest\bin"),
    (Join-Path $Sdk "platform-tools"),
    (Join-Path $Sdk "emulator")
) | Where-Object { $userPath -notlike "*$_*" }
if ($add) {
    [Environment]::SetEnvironmentVariable("Path", ($userPath.TrimEnd(";") + ";" + ($add -join ";")), "User")
}
Write-Ok "PATH atualizado (reabra o terminal para aplicar)"

# ---------------------------------------------------------------- 5. Licencas
Write-Step "Aceitando licencas do SDK"
(1..40 | ForEach-Object { "y" }) | & $SdkManager --sdk_root="$Sdk" --licenses 2>&1 | Out-Null
Write-Ok "Licencas aceitas"

# ---------------------------------------------------------------- 6. Componentes
Write-Step "Instalando componentes do SDK"
$packages = @(
    "platform-tools",
    "emulator",
    "platforms;android-$ApiLevel",
    "build-tools;$ApiLevel.0.0",
    "system-images;android-$ApiLevel;$SystemImageTag;x86_64"
)
& $SdkManager --sdk_root="$Sdk" @packages 2>&1 | Out-Null
Write-Ok "Instalado: $($packages -join ', ')"

# ---------------------------------------------------------------- 7. Flutter
Write-Step "Apontando o Flutter para o SDK"
if (Get-Command flutter -ErrorAction SilentlyContinue) {
    flutter config --android-sdk "$Sdk" 2>&1 | Out-Host
    Write-Ok "flutter config --android-sdk $Sdk"
} else {
    Write-Warn "Flutter nao encontrado no PATH; execute manualmente: flutter config --android-sdk `"$Sdk`""
}

# ---------------------------------------------------------------- 8. AVD
Write-Step "Criando o AVD $AvdName"
$existing = (& cmd /c "`"$AvdManager`" list avd 2>&1" | Out-String)
if ($existing -match [regex]::Escape($AvdName)) {
    Write-Ok "AVD ja existe"
} else {
    "no" | & $AvdManager create avd -n $AvdName -k "system-images;android-$ApiLevel;$SystemImageTag;x86_64" --device $AvdDevice --force 2>&1 | Out-Null
    Write-Ok "AVD criado"
}

# ---------------------------------------------------------------- 9. Aceleracao
Write-Step "Verificando aceleracao de hardware"
$accel = Join-Path $Sdk "emulator\emulator.exe"
if (Test-Path $accel) {
    $out = (& cmd /c "`"$accel`" -accel-check 2>&1" | Out-String)
    if ($out -match "usable") { Write-Ok "Aceleracao OK (WHPX/Hyper-V)" }
    else { Write-Warn "Aceleracao nao disponivel: habilite Hyper-V + Windows Hypervisor Platform e a virtualizacao na BIOS." }
}

# ---------------------------------------------------------------- 10. Opcional: iniciar
if ($Launch) {
    Write-Step "Iniciando o emulador $AvdName"
    Start-Process -FilePath $accel -ArgumentList "-avd", $AvdName, "-no-boot-anim" -WorkingDirectory (Join-Path $Sdk "emulator")
    Start-Sleep -Seconds 45
    $adb = Join-Path $Sdk "platform-tools\adb.exe"
    if (Test-Path $adb) { & $adb devices 2>&1 | Out-Host }
}

Write-Host "`nConcluido. Feche e reabra o terminal e rode: flutter doctor -v" -ForegroundColor Green

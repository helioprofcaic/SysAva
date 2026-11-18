<#
.SYNOPSIS
    Bandeja (tray) do SysAva: abre os apps, mostra o estado dos servidores e
    inicia junto com o Windows (estilo LM Studio).

.DESCRIPTION
    Menu do icone:
      - status (SysAva 8501 / Model Manager 8001 / Servidor do laboratorio 5000)
      - Abrir SysAva (8501)
      - Apps > (Duplicatas 8502, Monitor Supabase 8503, SeducTec 8504,
                Planejamento 8510, Analise de Notas 8511)
      - Servidor do laboratorio > Abrir painel (busca o servidor atual na
        rede: porta local, cache, peers.txt e broadcast UDP 5001) / Iniciar / Parar
      - Copiar URL, Abrir pasta do projeto
      - Iniciar com o Windows (atalho na pasta Inicializar)
      - Sair

    Se o app ainda nao estiver rodando, clicar na entrada inicia o Streamlit
    na porta correspondente e abre o navegador.

.PARAMETER Instalar    Cria o atalho de inicializacao automatica.
.PARAMETER Remover     Remove o atalho de inicializacao automatica.
.PARAMETER Status      Mostra o estado atual no console e sai.
#>
[CmdletBinding()]
param(
    [switch]$Instalar,
    [switch]$Remover,
    [switch]$Status
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Venv = Join-Path $Root ".sysenv\Scripts"
$Streamlit = Join-Path $Venv "streamlit.exe"
$Python = Join-Path $Venv "python.exe"
$Pythonw = Join-Path $Venv "pythonw.exe"
$PluginDir = Join-Path $Root "data\repo\plugins"
$MonitorDir = Join-Path $PluginDir "monitor"
$Receiver = Join-Path $MonitorDir "lab_receiver.py"
$Logo = Join-Path $MonitorDir "logo_sysava.png"
if (-not (Test-Path -LiteralPath $Logo)) { $Logo = Join-Path $Root "assets\logo_sysava.png" }
$Vbs = Join-Path $Root "sysava_tray.vbs"
$AtalhoNome = "SysAva Bandeja.lnk"
$ServidorCache = Join-Path $env:LOCALAPPDATA "SysAva\servidor_tray.txt"
$AgentCache = Join-Path $MonitorDir "server_cache.txt"
$PeersFile = Join-Path $MonitorDir "peers.txt"
$DiscoveryPort = 5001
$DiscoveryMagic = "SYSAVA_DISCOVER"
$DiscoveryReply = "SYSAVA_SERVER"

$Apps = @(
    @{ Nome = "SysAva (principal)";          Porta = 8501; Arq = "app.py" },
    @{ Nome = "Verificador de Duplicatas";   Porta = 8502; Arq = "apps\duplicate_checker\duplicate_checker_streamlit.py" },
    @{ Nome = "Monitor do Supabase";         Porta = 8503; Arq = "apps\supabase_monitor\supabase_monitor_streamlit.py" },
    @{ Nome = "Down SeducTec";               Porta = 8504; Arq = "apps\down_seductec\down_seductec_streamlit.py" },
    @{ Nome = "Planejamento e Registro";     Porta = 8510; Arq = "apps\planejamento_registro\planejamento_registro_streamlit.py" },
    @{ Nome = "Analise de Notas";            Porta = 8511; Arq = "apps\analise_notas\analise_notas_streamlit.py" }
)

# ---------------------------------------------------------------- utilidades
function Test-Porta {
    param([int]$P)
    $cli = $null
    try {
        $cli = New-Object System.Net.Sockets.TcpClient
        $ar = $cli.BeginConnect("127.0.0.1", $P, $null, $null)
        if ($ar.AsyncWaitHandle.WaitOne(300)) { return [bool]$cli.Connected }
        return $false
    } catch {
        return $false
    } finally {
        if ($cli) { $cli.Close() }
    }
}

function Get-IpLan {
    try {
        $cfg = (Get-NetIPConfiguration).Where({ $_.IPv4DefaultGateway -ne $null }) | Select-Object -First 1
        if ($cfg) { return $cfg.IPv4Address.IPAddress }
    } catch {}
    try {
        $ipa = Get-NetIPAddress -AddressFamily IPv4 |
            Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
            Select-Object -First 1
        if ($ipa) { return $ipa.IPAddress }
    } catch {}
    return "127.0.0.1"
}

function Get-RelUrl([int]$porta) {
    return "http://localhost:$porta/"
}

# --------------------------------------------- descoberta do servidor atual
function Get-BaseUrl([string]$url) {
    if (-not $url) { return $null }
    $u = $url.Trim()
    if (-not $u) { return $null }
    if ($u -notmatch '^https?://') { $u = "http://$u" }
    $u = $u.TrimEnd("/")
    if ($u -match '/ping$') { $u = $u.Substring(0, $u.Length - 5).TrimEnd("/") }
    return $u
}

function Test-SaudeUrl([string]$url) {
    $u = (Get-BaseUrl $url)
    if (-not $u) { return $false }
    try {
        $r = Invoke-RestMethod -Uri "$u/health" -TimeoutSec 1
        return ($r.status -eq "online")
    } catch {
        return $false
    }
}

function Get-PadroesServidorPreferido {
    # PC01 do laboratorio tem preferencia (SYSAVA_PREFERRED_SERVERS sobrescreve).
    $envServidores = [Environment]::GetEnvironmentVariable("SYSAVA_PREFERRED_SERVERS")
    if ($null -eq $envServidores) { return @("PC01*") }
    return @($envServidores -split '[,;]' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
}

function Test-ServidorPreferido([string]$url) {
    $u = (Get-BaseUrl $url)
    if (-not $u) { return $false }
    try {
        $r = Invoke-RestMethod -Uri "$u/health" -TimeoutSec 1
        if ($r.status -ne "online") { return $false }
        if ($r.preferred -eq $true) { return $true }
        $hostname = [string]$r.hostname
        if (-not $hostname) { $hostname = [string]$r.server_id }
        if (-not $hostname) { return $false }
        foreach ($padrao in (Get-PadroesServidorPreferido)) {
            if ($hostname -like $padrao) { return $true }
        }
    } catch {}
    return $false
}

function Sort-ServidoresPreferidos {
    param([string[]]$Urls)
    $preferidos = New-Object System.Collections.Generic.List[string]
    $outros = New-Object System.Collections.Generic.List[string]
    foreach ($u in @($Urls)) {
        $b = Get-BaseUrl $u
        if (-not $b) { continue }
        if (Test-ServidorPreferido $b) { if (-not $preferidos.Contains($b)) { $preferidos.Add($b) } }
        elseif (-not $outros.Contains($b)) { $outros.Add($b) }
    }
    return @($preferidos) + @($outros)
}

function Get-TailscaleCandidatos {
    # Servidores do tailnet (ex.: PC01) mesmo fora da LAN (casa/4G).
    $lista = New-Object System.Collections.Generic.List[string]
    try {
        $raw = & tailscale status --json 2>$null
        if (-not $raw) { return @() }
        $j = $raw | ConvertFrom-Json
        $peers = @($j.Peer.PSObject.Properties.Value)
        foreach ($p in $peers) {
            if (-not $p -or -not $p.Online) { continue }
            $ip = @($p.TailscaleIPs | Where-Object { $_ -match '^\d+\.' -and $_ -notmatch ':' } | Select-Object -First 1)
            if ($ip) {
                $u = "http://$($ip):5000"
                if (-not $lista.Contains($u)) { $lista.Add($u) }
            }
        }
    } catch {}
    return @($lista)
}

function Get-ServidorCandidatos {
    $lista = New-Object System.Collections.Generic.List[string]
    if (Test-Porta 5000) { $lista.Add("http://$(Get-IpLan):5000") }
    foreach ($f in @($ServidorCache, $AgentCache)) {
        try {
            if (Test-Path -LiteralPath $f) {
                $u = (Get-Content -LiteralPath $f -Raw -ErrorAction Stop).Trim()
                if ($u) { $lista.Add($u) }
            }
        } catch {}
    }
    try {
        if (Test-Path -LiteralPath $PeersFile) {
            foreach ($linha in (Get-Content -LiteralPath $PeersFile -ErrorAction Stop)) {
                $u = $linha.Trim()
                if ($u -match '^https?://') { $lista.Add($u) }
            }
        }
    } catch {}
    foreach ($u in (Get-TailscaleCandidatos)) {
        if ($u -and -not $lista.Contains($u)) { $lista.Add($u) }
    }
    return @($lista | Where-Object { $_ } | Select-Object -Unique)
}

function Find-ServidorUdp {
    $udp = $null
    try {
        $udp = New-Object System.Net.Sockets.UdpClient
        $udp.EnableBroadcast = $true
        $msg = [System.Text.Encoding]::ASCII.GetBytes($DiscoveryMagic)
        $alvos = @("255.255.255.255")
        $lan = Get-IpLan
        if ($lan -match '^(\d+\.\d+\.\d+)\.') { $alvos += "$($Matches[1]).255" }
        $alvos += @("192.168.10.255", "192.168.11.255")
        foreach ($t in ($alvos | Select-Object -Unique)) {
            try {
                $ep = New-Object System.Net.IPEndPoint -ArgumentList ([System.Net.IPAddress]::Parse($t)), $DiscoveryPort
                [void]$udp.Send($msg, $msg.Length, $ep)
            } catch {}
        }
        $udp.Client.ReceiveTimeout = 900
        $limite = [DateTime]::Now.AddSeconds(2)
        while ([DateTime]::Now -lt $limite) {
            try {
                $remoto = New-Object System.Net.IPEndPoint -ArgumentList ([System.Net.IPAddress]::Any), 0
                $dados = $udp.Receive([ref]$remoto)
                $txt = [System.Text.Encoding]::ASCII.GetString($dados).Trim()
                if ($txt -like "$DiscoveryReply*") {
                    $valor = ($txt.Substring($DiscoveryReply.Length).Trim() -split "`t")[0].Trim()
                    if ($valor -notmatch ":") { $valor = "$($remoto.Address.IPAddressToString):5000" }
                    $url = "http://$valor"
                    if (Test-SaudeUrl $url) { return (Get-BaseUrl $url) }
                }
            } catch [System.Net.Sockets.SocketException] { break }
        }
    } catch {} finally { if ($udp) { $udp.Close() } }
    return $null
}

function Find-ServidorUrl {
    $lista = @(Find-Servidores)
    if ($lista.Count -gt 0) { return $lista[0] }
    return (Find-ServidorUdp)
}

function Find-ServidoresUdp {
    $achados = New-Object System.Collections.Generic.List[string]
    $udp = $null
    try {
        $udp = New-Object System.Net.Sockets.UdpClient
        $udp.EnableBroadcast = $true
        $msg = [System.Text.Encoding]::ASCII.GetBytes($DiscoveryMagic)
        $alvos = @("255.255.255.255")
        $lan = Get-IpLan
        if ($lan -match '^(\d+\.\d+\.\d+)\.') { $alvos += "$($Matches[1]).255" }
        $alvos += @("192.168.10.255", "192.168.11.255")
        foreach ($t in ($alvos | Select-Object -Unique)) {
            try {
                $ep = New-Object System.Net.IPEndPoint -ArgumentList ([System.Net.IPAddress]::Parse($t)), $DiscoveryPort
                [void]$udp.Send($msg, $msg.Length, $ep)
            } catch {}
        }
        $udp.Client.ReceiveTimeout = 900
        $limite = [DateTime]::Now.AddSeconds(2)
        while ([DateTime]::Now -lt $limite) {
            try {
                $remoto = New-Object System.Net.IPEndPoint -ArgumentList ([System.Net.IPAddress]::Any), 0
                $dados = $udp.Receive([ref]$remoto)
                $txt = [System.Text.Encoding]::ASCII.GetString($dados).Trim()
                if ($txt -like "$DiscoveryReply*") {
                    $valor = ($txt.Substring($DiscoveryReply.Length).Trim() -split "`t")[0].Trim()
                    if ($valor -notmatch ":") { $valor = "$($remoto.Address.IPAddressToString):5000" }
                    $url = Get-BaseUrl "http://$valor"
                    if ($url -and (Test-SaudeUrl $url) -and -not $achados.Contains($url)) { $achados.Add($url) }
                }
            } catch [System.Net.Sockets.SocketException] { break }
        }
    } catch {} finally { if ($udp) { $udp.Close() } }
    return @($achados)
}

function Find-Servidores {
    $urls = New-Object System.Collections.Generic.List[string]
    foreach ($u in (Get-ServidorCandidatos)) {
        if (Test-SaudeUrl $u) {
            $b = Get-BaseUrl $u
            if ($b -and -not $urls.Contains($b)) { $urls.Add($b) }
        }
    }
    # Peers conhecidos pelo receiver local (notebook <-> PC do laboratorio).
    if (Test-Porta 5000) {
        try {
            $ps = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/peer/state" -TimeoutSec 2
            foreach ($p in @($ps.peers)) {
                if ($p -and (Test-SaudeUrl $p)) {
                    $b = Get-BaseUrl $p
                    if ($b -and -not $urls.Contains($b)) { $urls.Add($b) }
                }
            }
        } catch {}
    }
    foreach ($u in (Find-ServidoresUdp)) {
        if (-not $urls.Contains($u)) { $urls.Add($u) }
    }
    return @(Sort-ServidoresPreferidos -Urls @($urls))
}

function Save-ServidorCache([string]$url) {
    try {
        $dir = Split-Path -Parent $ServidorCache
        if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        Set-Content -LiteralPath $ServidorCache -Value $url -Encoding ASCII
    } catch {}
}

function Start-App($app) {
    if (Test-Porta $app.Porta) { return "ja-rodando" }
    if (-not (Test-Path -LiteralPath (Join-Path $Root $app.Arq))) { return "sem-arquivo" }
    if (-not (Test-Path -LiteralPath $Streamlit)) { return "sem-streamlit" }
    Start-Process -FilePath $Streamlit `
        -ArgumentList @("run", "`"$($app.Arq)`"", "--server.port", "$($app.Porta)", "--server.headless", "true") `
        -WorkingDirectory $Root -WindowStyle Hidden
    return "iniciado"
}

function Open-App($app) {
    $r = Start-App $app
    if ($r -eq "iniciado") {
        for ($i = 0; $i -lt 40; $i++) {
            if (Test-Porta $app.Porta) { break }
            Start-Sleep -Milliseconds 500
        }
    }
    Start-Process (Get-RelUrl $app.Porta)
    return $r
}

function Stop-Porta([int]$porta) {
    $con = Get-NetTCPConnection -LocalPort $porta -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $con) { return "ja-parado" }
    try {
        Stop-Process -Id $con.OwningProcess -Force -ErrorAction Stop
        return "parado"
    } catch {
        return "sem-permissao"
    }
}

function Start-Receiver {
    if (Test-Porta 5000) { return "ja-rodando" }
    if (-not (Test-Path -LiteralPath $Receiver)) { return "sem-receiver" }
    $py = if (Test-Path -LiteralPath $Pythonw) { $Pythonw } elseif (Test-Path -LiteralPath $Python) { $Python } else { $null }
    if (-not $py) { return "sem-python" }
    Start-Process -FilePath $py -ArgumentList "`"$Receiver`"" -WorkingDirectory $MonitorDir -WindowStyle Hidden
    return "iniciado"
}

function Get-AtalhoPath {
    Join-Path ([Environment]::GetFolderPath("Startup")) $AtalhoNome
}

function Install-AutoStart {
    if (-not (Test-Path -LiteralPath $Vbs)) { return $false }
    $lnk = Get-AtalhoPath
    $sh = New-Object -ComObject WScript.Shell
    $s = $sh.CreateShortcut($lnk)
    $s.TargetPath = Join-Path $env:SystemRoot "System32\wscript.exe"
    $s.Arguments = "`"$Vbs`""
    $s.WorkingDirectory = $Root
    $s.WindowStyle = 7
    $s.IconLocation = "$env:SystemRoot\System32\shell32.dll,13"
    $s.Description = "SysAva - bandeja dos apps e servidores"
    $s.Save()
    return (Test-Path -LiteralPath $lnk)
}

function Remove-AutoStart {
    $lnk = Get-AtalhoPath
    if (Test-Path -LiteralPath $lnk) { Remove-Item -LiteralPath $lnk -Force }
    return -not (Test-Path -LiteralPath $lnk)
}

# --------------------------------------------------- modos de linha de comando
if ($Instalar -or $Remover) {
    if ($Remover) {
        $ok = Remove-AutoStart
        Write-Host $(if ($ok) { "[OK] Inicializacao automatica removida." } else { "[ERRO] Nao consegui remover o atalho." }) `
            -ForegroundColor $(if ($ok) { "Green" } else { "Red" })
    }
    if ($Instalar) {
        $ok = Install-AutoStart
        Write-Host $(if ($ok) { "[OK] A bandeja vai iniciar junto com o Windows deste usuario." } else { "[ERRO] Nao consegui criar o atalho (sysava_tray.vbs existe?)." }) `
            -ForegroundColor $(if ($ok) { "Green" } else { "Red" })
        Write-Host "Atalho: $(Get-AtalhoPath)" -ForegroundColor Gray
    }
    exit 0
}

if ($Status) {
    Write-Host "Pasta:      $Root"
    foreach ($app in $Apps) {
        Write-Host ("  {0,-26} porta {1}: {2}" -f $app.Nome, $app.Porta, $(if (Test-Porta $app.Porta) { "online" } else { "offline" }))
    }
    Write-Host ("  {0,-26} porta {1}: {2}" -f "Servidor do laboratorio", 5000, $(if (Test-Porta 5000) { "online" } else { "offline" }))
    Write-Host ("  {0,-26} porta {1}: {2}" -f "Model Manager API", 8001, $(if (Test-Porta 8001) { "online" } else { "offline" }))
    $listaSrv = @(Find-Servidores)
    $srvUrl = $(if ($listaSrv.Count -gt 0) { $listaSrv[0] } else { $null })
    Write-Host ("  {0,-26} {1}" -f "Servidor atual", $(if ($srvUrl) { $srvUrl } else { "nao encontrado" }))
    Write-Host ("  {0,-26} {1}" -f "Servidores encontrados", $(if ($listaSrv.Count -gt 0) { $listaSrv -join ", " } else { "nenhum" }))
    Write-Host "Atalho:     $(if (Test-Path -LiteralPath (Get-AtalhoPath)) { 'instalado' } else { 'ausente' })"
    Write-Host "IP:         $(Get-IpLan)"
    exit 0
}

# ------------------------------------------------------------------- bandeja
try {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
} catch {
    Write-Host "[ERRO] Windows Forms indisponivel: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

$script:criado = $false
$mutex = New-Object System.Threading.Mutex($true, "Local\SysAvaTrayApps", [ref]$script:criado)
if (-not $script:criado) {
    Write-Host "[INFO] A bandeja do SysAva ja esta aberta nesta sessao." -ForegroundColor Yellow
    exit 0
}

# --- Monitor de portas em segundo plano (nao travar o menu) ---
$estado = [hashtable]::Synchronized(@{
    App = @{}; Servidor = $false; ModelApi = $false; Ip = (Get-IpLan)
    ServidorIp = "http://$(Get-IpLan):5000"; ServidorUrl = $null; ServidorRemoto = $false
    Servidores = @()
})
$pollScript = {
    param($state, $portas, $cacheFiles, $peersFile)
    function Get-Base([string]$url) {
        if (-not $url) { return $null }
        $u = $url.Trim()
        if (-not $u) { return $null }
        if ($u -notmatch '^https?://') { $u = "http://$u" }
        $u = $u.TrimEnd("/")
        if ($u -match '/ping$') { $u = $u.Substring(0, $u.Length - 5).TrimEnd("/") }
        return $u
    }
    function Test-Saude([string]$url) {
        $u = Get-Base $url
        if (-not $u) { return $false }
        try {
            $r = Invoke-RestMethod -Uri "$u/health" -TimeoutSec 1
            return ($r.status -eq "online")
        } catch { return $false }
    }
    function Get-Conhecido {
        foreach ($f in $cacheFiles) {
            try {
                if (Test-Path -LiteralPath $f) {
                    $u = (Get-Content -LiteralPath $f -Raw -ErrorAction Stop).Trim()
                    if ($u -and (Test-Saude $u)) { return (Get-Base $u) }
                }
            } catch {}
        }
        try {
            if ($peersFile -and (Test-Path -LiteralPath $peersFile)) {
                foreach ($linha in (Get-Content -LiteralPath $peersFile -ErrorAction Stop)) {
                    $u = $linha.Trim()
                    if ($u -match '^https?://' -and (Test-Saude $u)) { return (Get-Base $u) }
                }
            }
        } catch {}
        return $null
    }
    $ciclo = 0
    while ($true) {
        foreach ($p in $portas) {
            $cli = $null
            $aberta = $false
            try {
                $cli = New-Object System.Net.Sockets.TcpClient
                $ar = $cli.BeginConnect("127.0.0.1", [int]$p, $null, $null)
                if ($ar.AsyncWaitHandle.WaitOne(300)) { $aberta = [bool]$cli.Connected }
            } catch { $aberta = $false } finally { if ($cli) { $cli.Close() } }
            $state.App[[int]$p] = $aberta
        }
        $state.Servidor = [bool]$state.App[5000]
        $state.ModelApi = [bool]$state.App[8001]
        if ($ciclo % 10 -eq 0) {
            try {
                $cfg = (Get-NetIPConfiguration).Where({ $_.IPv4DefaultGateway -ne $null }) | Select-Object -First 1
                if ($cfg) {
                    $novoIp = [string]$cfg.IPv4Address.IPAddress
                    if ($novoIp) {
                        $state.Ip = $novoIp
                        $state.ServidorIp = "http://${novoIp}:5000"
                    }
                }
            } catch {}
        }
        $ciclo++
        Start-Sleep -Milliseconds 2500
    }
}
$runspace = [runspacefactory]::CreateRunspace()
$runspace.ApartmentState = "MTA"
$runspace.ThreadOptions = "ReuseThread"
$runspace.Open()
$poll = [powershell]::Create()
$poll.Runspace = $runspace
[void]$poll.AddScript($pollScript).AddArgument($estado).AddArgument(@(8001, 5000, 8501, 8502, 8503, 8504, 8510, 8511)).AddArgument(@($ServidorCache, $AgentCache)).AddArgument($PeersFile)
$pollHandle = $poll.BeginInvoke()

# --- Descoberta periÃ³dica de TODOS os servidores (notebook + PC do laboratorio) ---
$srvPollScript = {
    param($state, $cacheFiles, $peersFile, $discoveryPort, $receiverApi)
    function Get-Base([string]$url) {
        if (-not $url) { return $null }
        $u = $url.Trim()
        if (-not $u) { return $null }
        if ($u -notmatch '^https?://') { $u = "http://$u" }
        $u = $u.TrimEnd("/")
        if ($u -match '/ping$') { $u = $u.Substring(0, $u.Length - 5).TrimEnd("/") }
        return $u
    }
    function Test-Saude([string]$url) {
        $u = Get-Base $url
        if (-not $u) { return $false }
        try {
            $r = Invoke-RestMethod -Uri "$u/health" -TimeoutSec 1
            return ($r.status -eq "online")
        } catch { return $false }
    }
    function Test-Preferido([string]$url) {
        $u = Get-Base $url
        if (-not $u) { return $false }
        try {
            $r = Invoke-RestMethod -Uri "$u/health" -TimeoutSec 1
            if ($r.status -ne "online") { return $false }
            if ($r.preferred -eq $true) { return $true }
            $hostname = [string]$r.hostname
            if (-not $hostname) { $hostname = [string]$r.server_id }
            if (-not $hostname) { return $false }
            $envServidores = [Environment]::GetEnvironmentVariable("SYSAVA_PREFERRED_SERVERS")
            $padroes = if ($null -eq $envServidores) { @("PC01*") } else { @($envServidores -split '[,;]' | ForEach-Object { $_.Trim() } | Where-Object { $_ }) }
            foreach ($padrao in $padroes) { if ($hostname -like $padrao) { return $true } }
        } catch {}
        return $false
    }
    function Get-Udp {
        $achados = New-Object System.Collections.Generic.List[string]
        $udp = $null
        try {
            $udp = New-Object System.Net.Sockets.UdpClient
            $udp.EnableBroadcast = $true
            $msg = [System.Text.Encoding]::ASCII.GetBytes("SYSAVA_DISCOVER")
            $alvos = @("255.255.255.255")
            if ($state.Ip -match '^(\d+\.\d+\.\d+)\.') { $alvos += "$($Matches[1]).255" }
            $alvos += @("192.168.10.255", "192.168.11.255")
            foreach ($t in ($alvos | Select-Object -Unique)) {
                try {
                    $ep = New-Object System.Net.IPEndPoint -ArgumentList ([System.Net.IPAddress]::Parse($t)), $discoveryPort
                    [void]$udp.Send($msg, $msg.Length, $ep)
                } catch {}
            }
            $udp.Client.ReceiveTimeout = 900
            $limite = [DateTime]::Now.AddSeconds(2)
            while ([DateTime]::Now -lt $limite) {
                try {
                    $remoto = New-Object System.Net.IPEndPoint -ArgumentList ([System.Net.IPAddress]::Any), 0
                    $dados = $udp.Receive([ref]$remoto)
                    $txt = [System.Text.Encoding]::ASCII.GetString($dados).Trim()
                    if ($txt -like "SYSAVA_SERVER*") {
                        $valor = ($txt.Substring(13).Trim() -split "`t")[0].Trim()
                        if ($valor -notmatch ":") { $valor = "$($remoto.Address.IPAddressToString):5000" }
                        $b = Get-Base "http://$valor"
                        if ($b -and (Test-Saude $b) -and -not $achados.Contains($b)) { $achados.Add($b) }
                    }
                } catch [System.Net.Sockets.SocketException] { break }
            }
        } catch {} finally { if ($udp) { $udp.Close() } }
        return @($achados)
    }
    while ($true) {
        $urls = New-Object System.Collections.Generic.List[string]
        if ($state.App[5000]) { $urls.Add($state.ServidorIp) }
        foreach ($f in $cacheFiles) {
            try {
                if (Test-Path -LiteralPath $f) {
                    $u = (Get-Content -LiteralPath $f -Raw -ErrorAction Stop).Trim()
                    if ($u) { $urls.Add($u) }
                }
            } catch {}
        }
        try {
            if ($peersFile -and (Test-Path -LiteralPath $peersFile)) {
                foreach ($linha in (Get-Content -LiteralPath $peersFile -ErrorAction Stop)) {
                    $u = $linha.Trim()
                    if ($u -match '^https?://') { $urls.Add($u) }
                }
            }
        } catch {}
        try {
            if ($state.App[5000]) {
                $ps = Invoke-RestMethod -Uri "$receiverApi/api/peer/state" -TimeoutSec 2
                foreach ($p in @($ps.peers)) { if ($p) { $urls.Add($p) } }
            }
        } catch {}
        foreach ($u in (Get-Udp)) { $urls.Add($u) }
        # Tambem procura no tailnet (PC01 acessivel de casa/4G).
        try {
            $raw = & tailscale status --json 2>$null
            if ($raw) {
                $j = $raw | ConvertFrom-Json
                foreach ($p in @($j.Peer.PSObject.Properties.Value)) {
                    if (-not $p -or -not $p.Online) { continue }
                    $ip = @($p.TailscaleIPs | Where-Object { $_ -match '^\d+\.' -and $_ -notmatch ':' } | Select-Object -First 1)
                    if ($ip) { $urls.Add("http://$($ip):5000") }
                }
            }
        } catch {}
        $ok = New-Object System.Collections.Generic.List[string]
        foreach ($u in ($urls | Select-Object -Unique)) {
            if (Test-Saude $u) {
                $b = Get-Base $u
                if ($b -and -not $ok.Contains($b)) { $ok.Add($b) }
            }
        }
        $preferidos = New-Object System.Collections.Generic.List[string]
        $outros = New-Object System.Collections.Generic.List[string]
        foreach ($u in $ok) {
            if (Test-Preferido $u) { $preferidos.Add($u) } else { $outros.Add($u) }
        }
        $ordenado = @($preferidos) + @($outros)
        $state.Servidores = @($ordenado)
        $state.ServidorUrl = $(if ($ordenado.Count -gt 0) { $ordenado[0] } else { $null })
        $state.ServidorRemoto = $false
        Start-Sleep -Seconds 20
    }
}
$runspace2 = [runspacefactory]::CreateRunspace()
$runspace2.ApartmentState = "MTA"
$runspace2.ThreadOptions = "ReuseThread"
$runspace2.Open()
$srvPoll = [powershell]::Create()
$srvPoll.Runspace = $runspace2
[void]$srvPoll.AddScript($srvPollScript).AddArgument($estado).AddArgument(@($ServidorCache, $AgentCache)).AddArgument($PeersFile).AddArgument($DiscoveryPort).AddArgument("http://127.0.0.1:5000")
$srvPollHandle = $srvPoll.BeginInvoke()

function New-Icone {
    param([System.Drawing.Color]$cor, [string]$letra = "S")
    if (Test-Path -LiteralPath $Logo) {
        try {
            $src = [System.Drawing.Image]::FromFile($Logo)
            $bmp = New-Object System.Drawing.Bitmap 32, 32
            $g = [System.Drawing.Graphics]::FromImage($bmp)
            $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $g.DrawImage($src, 0, 0, 32, 32)
            $g.Dispose()
            $src.Dispose()
            $hIcon = $bmp.GetHicon()
            $icone = [System.Drawing.Icon]::FromHandle($hIcon).Clone()
            $bmp.Dispose()
            return $icone
        } catch {}
    }
    $bmp = New-Object System.Drawing.Bitmap 16, 16
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.Clear([System.Drawing.Color]::Transparent)
    $brush = New-Object System.Drawing.SolidBrush $cor
    $g.FillEllipse($brush, 1, 1, 14, 14)
    $font = New-Object System.Drawing.Font "Segoe UI", 8, ([System.Drawing.FontStyle]::Bold), ([System.Drawing.GraphicsUnit]::Pixel)
    $g.DrawString($letra, $font, [System.Drawing.Brushes]::White, 4, 2)
    $g.Dispose()
    $hIcon = $bmp.GetHicon()
    $icone = [System.Drawing.Icon]::FromHandle($hIcon).Clone()
    $bmp.Dispose()
    return $icone
}

$corVerde = [System.Drawing.Color]::FromArgb(46, 204, 113)
$corAmarelo = [System.Drawing.Color]::FromArgb(241, 196, 15)
$corVermelho = [System.Drawing.Color]::FromArgb(231, 76, 60)
$corAzul = [System.Drawing.Color]::FromArgb(26, 115, 232)

$notify = New-Object System.Windows.Forms.NotifyIcon
$menu = New-Object System.Windows.Forms.ContextMenuStrip

$miTitulo = New-Object System.Windows.Forms.ToolStripMenuItem "SysAva"
$miTitulo.Enabled = $false
[void]$menu.Items.Add($miTitulo)
$miStatus = New-Object System.Windows.Forms.ToolStripMenuItem "verificando..."
$miStatus.Enabled = $false
[void]$menu.Items.Add($miStatus)
[void]$menu.Items.Add((New-Object System.Windows.Forms.ToolStripSeparator))

$miAbrir = New-Object System.Windows.Forms.ToolStripMenuItem "Abrir SysAva (8501)"
[void]$menu.Items.Add($miAbrir)

$miApps = New-Object System.Windows.Forms.ToolStripMenuItem "Apps"
foreach ($app in $Apps) {
    $item = New-Object System.Windows.Forms.ToolStripMenuItem ("{0}  ({1})" -f $app.Nome, $app.Porta)
    $item.Tag = $app
    $item.add_Click({
        $a = $app
        $r = Open-App $a
        if ($r -eq "iniciado") { Show-Balao "$($a.Nome) iniciando na porta $($a.Porta)..." }
        elseif ($r -eq "sem-arquivo") { Show-Balao "Arquivo do app nao encontrado: $($a.Arq)" "Warning" }
        elseif ($r -eq "sem-streamlit") { Show-Balao "Streamlit do .sysenv nao encontrado. Rode run.bat." "Warning" }
    }.GetNewClosure())
    [void]$miApps.DropDownItems.Add($item)
}
[void]$miApps.DropDownItems.Add((New-Object System.Windows.Forms.ToolStripSeparator))
$miPararApps = New-Object System.Windows.Forms.ToolStripMenuItem "Parar todos os apps"
[void]$miApps.DropDownItems.Add($miPararApps)
[void]$menu.Items.Add($miApps)

$miServidor = New-Object System.Windows.Forms.ToolStripMenuItem "Servidor do laboratorio (5000)"
[void]$menu.Items.Add($miServidor)
$miServidorAbrir = New-Object System.Windows.Forms.ToolStripMenuItem "Abrir painel do monitor"
$miServidorAbrir.ToolTipText = "Abre o servidor principal encontrado (porta local, cache, peers.txt e UDP)"
$miServidorSegundo = New-Object System.Windows.Forms.ToolStripMenuItem "Abrir painel do 2Âº servidor"
$miServidorSegundo.Enabled = $false
$miServidorSegundo.ToolTipText = "Abre o outro servidor SysAva encontrado na rede (notebook/PC do laboratorio)"
$miServidoresLista = New-Object System.Windows.Forms.ToolStripMenuItem "Servidores encontrados"
$miServidoresLista.Enabled = $false
$miServidorBuscar = New-Object System.Windows.Forms.ToolStripMenuItem "Buscar servidores na rede"
$miServidorBuscar.ToolTipText = "Descobre todos os servidores SysAva ativos agora"
$miServidorIniciar = New-Object System.Windows.Forms.ToolStripMenuItem "Iniciar servidor neste PC"
$miServidorParar = New-Object System.Windows.Forms.ToolStripMenuItem "Parar servidor deste PC"
[void]$miServidor.DropDownItems.Add($miServidorAbrir)
[void]$miServidor.DropDownItems.Add($miServidorSegundo)
[void]$miServidor.DropDownItems.Add($miServidoresLista)
[void]$miServidor.DropDownItems.Add($miServidorBuscar)
[void]$miServidor.DropDownItems.Add((New-Object System.Windows.Forms.ToolStripSeparator))
[void]$miServidor.DropDownItems.Add($miServidorIniciar)
[void]$miServidor.DropDownItems.Add($miServidorParar)

[void]$menu.Items.Add((New-Object System.Windows.Forms.ToolStripSeparator))
$miCopiar = New-Object System.Windows.Forms.ToolStripMenuItem "Copiar URL do SysAva"
[void]$menu.Items.Add($miCopiar)
$miPasta = New-Object System.Windows.Forms.ToolStripMenuItem "Abrir pasta do projeto"
[void]$menu.Items.Add($miPasta)

[void]$menu.Items.Add((New-Object System.Windows.Forms.ToolStripSeparator))
$miAutoApp = New-Object System.Windows.Forms.ToolStripMenuItem "Abrir o SysAva ao iniciar a bandeja"
$FlagAutoApp = Join-Path $env:LOCALAPPDATA "SysAva\tray_autoapp.flag"
$miAutoApp.Checked = Test-Path -LiteralPath $FlagAutoApp
[void]$menu.Items.Add($miAutoApp)
$miAuto = New-Object System.Windows.Forms.ToolStripMenuItem "Iniciar com o Windows"
$miAuto.Checked = Test-Path -LiteralPath (Get-AtalhoPath)
[void]$menu.Items.Add($miAuto)
[void]$menu.Items.Add((New-Object System.Windows.Forms.ToolStripSeparator))
$miSair = New-Object System.Windows.Forms.ToolStripMenuItem "Sair da bandeja"
[void]$menu.Items.Add($miSair)

$notify.ContextMenuStrip = $menu
$notify.Text = "SysAva"
$notify.Icon = New-Icone $corAmarelo
$notify.Visible = $true

function Show-Balao {
    param([string]$texto, [string]$tipo = "Info")
    try {
        $notify.ShowBalloonTip(4000, "SysAva", $texto, [System.Windows.Forms.ToolTipIcon]::$tipo)
    } catch {}
}

$script:segundoUrl = $null
$script:servidoresSig = "__inicial__"

function Get-HostDoUrl([string]$url) {
    try { return ([uri]$url).Host } catch { return $url }
}

function Update-ServidoresMenu {
    $lista = @($estado.Servidores | Where-Object { $_ })
    $sig = $lista -join "|"
    if ($sig -eq $script:servidoresSig) { return }
    $script:servidoresSig = $sig

    $miServidoresLista.DropDownItems.Clear()
    if ($lista.Count -eq 0) {
        $vazio = New-Object System.Windows.Forms.ToolStripMenuItem "(nenhum encontrado)"
        $vazio.Enabled = $false
        [void]$miServidoresLista.DropDownItems.Add($vazio)
        $miServidoresLista.Enabled = $false
        $miServidorSegundo.Enabled = $false
        $script:segundoUrl = $null
        return
    }
    $miServidoresLista.Enabled = $true
    $localHost = [string]$estado.Ip
    foreach ($u in $lista) {
        $h = Get-HostDoUrl $u
        $rot = if ($h -eq $localHost) { "Local: $h" } else { "Servidor: $h" }
        $item = New-Object System.Windows.Forms.ToolStripMenuItem $rot
        $item.Tag = $u
        $item.ToolTipText = $u
        $item.add_Click({
            param($sender, $args)
            $alvo = [string]$sender.Tag
            if ($alvo) {
                Save-ServidorCache $alvo
                Start-Process $alvo
                Show-Balao "Abrindo $alvo"
            }
        })
        [void]$miServidoresLista.DropDownItems.Add($item)
    }
    $prim = [string]$estado.ServidorUrl
    $seg = $lista | Where-Object { $_ -ne $prim } | Select-Object -First 1
    if (-not $seg -and $lista.Count -gt 1) { $seg = $lista[1] }
    $script:segundoUrl = $seg
    $miServidorSegundo.Enabled = [bool]$seg
    if ($seg) { $miServidorSegundo.Text = "Abrir painel do 2Âº servidor ($(Get-HostDoUrl $seg))" }
    else { $miServidorSegundo.Text = "Abrir painel do 2Âº servidor" }
    if ($prim) { $miServidorAbrir.Text = "Abrir painel do monitor ($(Get-HostDoUrl $prim))" }
}

$appPrincipal = $Apps | Where-Object { $_.Porta -eq 8501 } | Select-Object -First 1

$miAbrir.add_Click({
    $r = Open-App $appPrincipal
    if ($r -eq "iniciado") { Show-Balao "SysAva iniciando na porta 8501..." }
    elseif ($r -eq "sem-streamlit") { Show-Balao "Streamlit do .sysenv nao encontrado. Rode run.bat." "Warning" }
})
$miPararApps.add_Click({
    $parados = 0
    foreach ($a in $Apps) { if ((Stop-Porta $a.Porta) -eq "parado") { $parados++ } }
    Show-Balao $(if ($parados) { "$parados app(s) encerrado(s)." } else { "Nenhum app estava rodando." })
})
$miServidorAbrir.add_Click({
    $url = $estado.ServidorUrl
    if (-not $url) { $url = Find-ServidorUrl }
    if ($url) {
        $estado.ServidorUrl = $url
        Save-ServidorCache $url
        Start-Process $url
        Show-Balao "Abrindo o servidor em $url"
    } else {
        Show-Balao "Nao encontrei o servidor SysAva na rede. Ligue o PC servidor ou rode o diagnostico_servidor.bat." "Warning"
    }
})
$miServidorSegundo.add_Click({
    $url = $script:segundoUrl
    if (-not $url) {
        $lista = @($estado.Servidores | Where-Object { $_ })
        $prim = [string]$estado.ServidorUrl
        $url = $lista | Where-Object { $_ -ne $prim } | Select-Object -First 1
    }
    if ($url) {
        Save-ServidorCache $url
        Start-Process $url
        Show-Balao "Abrindo o 2Âº servidor em $url"
    } else {
        Show-Balao "Nenhum segundo servidor encontrado. Use 'Buscar servidores na rede'." "Warning"
    }
})
$miServidorBuscar.add_Click({
    $lista = @(Find-Servidores)
    $estado.Servidores = @($lista)
    $estado.ServidorUrl = $(if ($lista.Count -gt 0) { $lista[0] } else { $null })
    if ($lista.Count -gt 0) {
        Save-ServidorCache $lista[0]
        $hosts = @($lista | ForEach-Object { Get-HostDoUrl $_ }) -join ", "
        $miServidor.Text = "Servidor do laboratorio (5000) - $($lista.Count) encontrado(s): $hosts"
        Show-Balao "Servidores encontrados: $hosts"
    } else {
        $miServidor.Text = "Servidor do laboratorio (5000) - offline"
        Show-Balao "Nenhum servidor SysAva respondeu na rede." "Warning"
    }
    $script:servidoresSig = "__inicial__"
    Update-ServidoresMenu
})
$miServidorIniciar.add_Click({
    $r = Start-Receiver
    switch ($r) {
        "iniciado" { Show-Balao "Servidor do laboratorio iniciando..." }
        "ja-rodando" { Show-Balao "O servidor ja esta rodando." }
        "sem-python" { Show-Balao "Python do .sysenv nao encontrado. Rode run.bat." "Warning" }
        default { Show-Balao "Nao consegui iniciar o servidor ($r)." "Error" }
    }
})
$miServidorParar.add_Click({
    $r = Stop-Porta 5000
    if ($r -eq "sem-permissao") { Show-Balao "Sem permissao para parar o servidor (pode ser tarefa SYSTEM)." "Warning" }
    else { Show-Balao "Servidor do laboratorio parado." }
})
$miCopiar.add_Click({
    try {
        [System.Windows.Forms.Clipboard]::SetText((Get-RelUrl 8501))
        Show-Balao "URL copiada: $(Get-RelUrl 8501)"
    } catch {}
})
$miPasta.add_Click({
    Start-Process explorer.exe -ArgumentList "`"$Root`""
})
$miAutoApp.add_Click({
    try {
        if ($miAutoApp.Checked) {
            Remove-Item -LiteralPath $FlagAutoApp -Force -ErrorAction SilentlyContinue
            $miAutoApp.Checked = $false
            Show-Balao "O SysAva nao abre mais sozinho com a bandeja."
        } else {
            New-Item -ItemType Directory -Path (Split-Path -Parent $FlagAutoApp) -Force | Out-Null
            Set-Content -LiteralPath $FlagAutoApp -Value "1" -Encoding ASCII
            $miAutoApp.Checked = $true
            Show-Balao "O SysAva vai abrir ao iniciar a bandeja (no logon)."
        }
    } catch {
        Show-Balao "Nao consegui salvar a opcao: $($_.Exception.Message)" "Warning"
    }
})

$miAuto.add_Click({
    if ($miAuto.Checked) {
        if (Remove-AutoStart) { $miAuto.Checked = $false; Show-Balao "Removido da inicializacao do Windows." }
        else { Show-Balao "Nao consegui remover o atalho." "Warning" }
    } else {
        if (Install-AutoStart) { $miAuto.Checked = $true; Show-Balao "A bandeja vai abrir junto com o Windows." }
        else { Show-Balao "Nao consegui criar o atalho (sysava_tray.vbs existe?)." "Warning" }
    }
})
$miSair.add_Click({
    $timer.Stop()
    $notify.Visible = $false
    $notify.Dispose()
    $menu.Dispose()
    try { $poll.Stop() } catch {}
    try { $runspace.Dispose() } catch {}
    try { $srvPoll.Stop() } catch {}
    try { $runspace2.Dispose() } catch {}
    try { $mutex.ReleaseMutex() } catch {}
    [System.Windows.Forms.Application]::ExitThread()
})

$script:assinatura = ""
$script:temLogo = Test-Path -LiteralPath $Logo
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 1500
$timer.add_Tick({
    Update-ServidoresMenu
    $appOn = [bool]$estado.App[8501]
    $srvLocalOn = [bool]$estado.Servidor
    $srvUrl = $estado.ServidorUrl
    $srvOn = $srvLocalOn -or [bool]$srvUrl
    $apiOn = [bool]$estado.ModelApi
    $listaSrv = @($estado.Servidores | Where-Object { $_ })
    $assinatura = (@($Apps | ForEach-Object { [int]$estado.App[[int]$_.Porta] }) -join "") + "|$srvOn|$apiOn|$srvUrl|$($listaSrv -join ',')"
    if ($assinatura -eq $script:assinatura) { return }
    $script:assinatura = $assinatura

    $hostSrv = $null
    if ($srvUrl) { try { $hostSrv = ([uri]$srvUrl).Host } catch {} }
    if (-not $hostSrv -and $srvLocalOn) { $hostSrv = [string]$estado.Ip }
    $qtdSrv = $listaSrv.Count

    if ($script:temLogo) {
        # Com o logo, o status aparece no texto do menu e no tooltip.
    } elseif ($appOn) {
        $notify.Icon = New-Icone $corVerde
    } elseif ($srvOn -or $apiOn) {
        $notify.Icon = New-Icone $corAmarelo
    } else {
        $notify.Icon = New-Icone $corVermelho
    }
    $miStatus.Text = "SysAva: $(if ($appOn) { 'online' } else { 'offline' }) na porta 8501"
    $notify.Text = "SysAva 8501: $(if ($appOn) { 'online' } else { 'offline' }) | Servidor: $(if ($srvOn) { 'online' } else { 'offline' })$(if ($hostSrv) { " ($hostSrv)" } else { '' }) | $qtdSrv encontrado(s)"
    $miAbrir.Text = "Abrir SysAva (8501) - $(if ($appOn) { 'online' } else { 'iniciar' })"
    $miTitulo.Text = "SysAva | Servidor: $(if ($hostSrv) { $hostSrv } else { 'procurando...' })"
    if ($srvLocalOn) {
        $miServidor.Text = "Servidor do laboratorio (5000) - online NESTE PC"
    } elseif ($srvUrl) {
        $extra = if ($qtdSrv -gt 1) { " - $qtdSrv encontrados" } else { "" }
        $miServidor.Text = "Servidor encontrado: $hostSrv$extra (este PC offline)"
    } else {
        $miServidor.Text = "Servidor do laboratorio (5000) - offline neste PC"
    }
    # "Iniciar servidor" vale para ESTE PC. Um servidor remoto (notebook)
    # encontrado na rede nao impede subir o servidor local do PC01.
    $miServidorIniciar.Enabled = -not $srvLocalOn
    $miServidorParar.Enabled = $srvLocalOn
    foreach ($item in $miApps.DropDownItems) {
        if ($item -is [System.Windows.Forms.ToolStripMenuItem] -and $item.Tag) {
            $item.Text = "{0}  ({1}){2}" -f $item.Tag.Nome, $item.Tag.Porta, $(if ($estado.App[[int]$item.Tag.Porta]) { "  â€¢" } else { "" })
        }
    }
})
$timer.Start()

# Opcional: abrir o SysAva assim que a bandeja inicia (marcado no menu).
if ($miAutoApp.Checked -and $appPrincipal) {
    [void](Open-App $appPrincipal)
    Show-Balao "SysAva iniciando na porta 8501..."
}

[System.Windows.Forms.Application]::Run()

<#
.SYNOPSIS
    Script interativo para gerenciar Git commits no SysAva com segurança.
#>

$ErrorActionPreference = "Continue"

function Show-Header {
    Clear-Host
    Write-Host "==========================================" -ForegroundColor Magenta
    Write-Host "   🚀 SysAva Git Assistant" -ForegroundColor Magenta
    Write-Host "==========================================" -ForegroundColor Magenta
}

function Check-And-Set-Git-Config {
    $userName = git config user.name
    $userEmail = git config user.email

    if ([string]::IsNullOrWhiteSpace($userName)) {
        Write-Host "`n⚠️ O nome de usuário do Git não está configurado." -ForegroundColor Yellow
        $newName = Read-Host "   Digite seu nome completo (Ex: João Silva)"
        git config user.name "$newName"
        Write-Host "✅ Nome de usuário configurado como: $newName" -ForegroundColor Green
    }

    if ([string]::IsNullOrWhiteSpace($userEmail)) {
        Write-Host "`n⚠️ O e-mail do Git não está configurado." -ForegroundColor Yellow
        $newEmail = Read-Host "   Digite seu e-mail (o mesmo do GitHub)"
        git config user.email "$newEmail"
        Write-Host "✅ E-mail configurado como: $newEmail" -ForegroundColor Green
    }
}

while ($true) {
    Show-Header
    
    Write-Host "`n[ Status Atual (Resumido) ]" -ForegroundColor Cyan
    git status -s

    # Verifica a configuração do Git antes de mostrar o menu de commit
    Check-And-Set-Git-Config
    
    Write-Host "`nMenu de Comandos:" -ForegroundColor Yellow
    Write-Host "1. Preparar tudo (git add .)"
    Write-Host "2. Ver status detalhado (Antes de commit/push)"
    Write-Host "3. Criar Commit (Salvar alterações localmente)"
    Write-Host "4. Fazer Push (Enviar para o GitHub/Branch)"
    Write-Host "5. Fazer Pull (Baixar atualizações do servidor)"
    Write-Host "q. Sair"

    $choice = Read-Host "`nEscolha uma opção"

    switch ($choice) {
        "1" {
            git add .
            Write-Host "`nArquivos adicionados à fila de commit!" -ForegroundColor Green
            Start-Sleep -Seconds 1
        }
        "2" {
            Write-Host "`n[ Status Detalhado ]" -ForegroundColor Cyan
            git status
            Read-Host "`nPressione Enter para voltar ao menu..."
        }
        "3" {
            $msg = Read-Host "`nDigite a mensagem do commit"
            if (-not [string]::IsNullOrWhiteSpace($msg)) {
                git commit -m "$msg"
            } else {
                Write-Host "Erro: O commit precisa de uma mensagem!" -ForegroundColor Red
            }
            Read-Host "`nPressione Enter para continuar..."
        }
        "4" {
            $currentBranch = git branch --show-current
            Write-Host "`nSubindo alterações para a branch: $currentBranch..." -ForegroundColor Cyan
            git push origin $currentBranch
            Read-Host "`nPressione Enter para continuar..."
        }
        "5" {
            git pull
            Read-Host "`nPressione Enter para continuar..."
        }
        "q" {
            Write-Host "Até logo!" -ForegroundColor Gray
            break
        }
    }
}
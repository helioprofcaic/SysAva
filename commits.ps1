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

while ($true) {
    Show-Header
    
    Write-Host "`n[ Status Atual (Resumido) ]" -ForegroundColor Cyan
    git status -s
    
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
# Flutter no Windows: baixar, instalar e testar (guia rápido)

Este guia cobre **somente o Flutter SDK**. Ele não instala Android Studio,
emulador, JDK nem Android SDK. Para essa parte, use
`Android-sdk-tools-flutter.md` e `flutter-android-e-web.md`.

> Testado em Windows 10/11 64 bits. **Versão usada neste guia: Flutter 3.47.7 stable.**

---

## TL;DR — comando completo (copiar e colar)

Baixa o ZIP oficial, extrai em `C:\src`, coloca `C:\src\flutter\bin` no PATH
do usuário e testa a versão:

```powershell
$url = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.47.7-stable.zip"
$zip = "$env:USERPROFILE\Downloads\flutter_windows_3.47.7-stable.zip"

# 1) Baixar (se ainda não tiver o zip)
Invoke-WebRequest -Uri $url -OutFile $zip

# 2) Extrair em C:\src (o zip já cria a pasta "flutter")
New-Item -ItemType Directory -Path "C:\src" -Force | Out-Null
Expand-Archive -Path $zip -DestinationPath "C:\src" -Force
Test-Path "C:\src\flutter\bin\flutter.bat"   # deve retornar True

# 3) Colocar no PATH do usuário (na frente de qualquer Flutter antigo)
$bin = "C:\src\flutter\bin"
$p = [Environment]::GetEnvironmentVariable("Path", "User")
$partes = ($p -split ';') | Where-Object { $_ -and ($_ -ne $bin) }
[Environment]::SetEnvironmentVariable("Path", "$bin;" + ($partes -join ';'), "User")
$env:Path = "$bin;" + (($env:Path -split ';' | Where-Object { $_ -and ($_ -ne $bin) }) -join ';')

# 4) Testar
flutter --version
flutter doctor
```

> Abra um **terminal novo** depois do passo 3 para o PATH valer nos próximos
> comandos. Se já tem o zip em `Downloads`, pode pular o passo 1.

---

## 1. O que você precisa

- Windows 10 ou 11, 64 bits
- Cerca de **3 GB livres** em disco
- Internet (a primeira execução baixa componentes)
- **Git para Windows**
- PowerShell

---

## 2. Instalar o Git (se ainda não tiver)

Abra o PowerShell e rode:

```powershell
winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
```

Se o `winget` não existir, baixe em <https://git-scm.com/download/win>.
Depois **feche e abra o PowerShell** e confira:

```powershell
git --version
```

---

## 3. Baixar e extrair o Flutter 3.47.7

**Link direto do ZIP 3.47.7 stable:**

<https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.47.7-stable.zip>

1. Baixe o ZIP (o link acima ou <https://docs.flutter.dev/get-started/install/windows>).
   Por padrão ele fica em `%USERPROFILE%\Downloads`.
2. Extraia com o comando abaixo (a pasta `src` precisa existir):

```powershell
New-Item -ItemType Directory -Path "C:\src" -Force | Out-Null

Expand-Archive -Path "$env:USERPROFILE\Downloads\flutter_windows_3.47.7-stable.zip" -DestinationPath "C:\src" -Force

# Deve retornar True:
Test-Path "C:\src\flutter\bin\flutter.bat"
```

Se preferir baixar pelo PowerShell:

```powershell
Invoke-WebRequest `
  -Uri "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.47.7-stable.zip" `
  -OutFile "$env:USERPROFILE\Downloads\flutter_windows_3.47.7-stable.zip"
```

> **Atenção:** use `-DestinationPath "C:\src"`, e **não**
> `-DestinationPath "C:\src\flutter"`. O zip já cria a pasta `flutter` dentro
> do destino; extrair em `C:\src\flutter` gera `C:\src\flutter\flutter\bin`.
> Também não use `"$env:C:\..."`: o correto é `$env:USERPROFILE` ou o caminho
> normal `"C:\src"`.

O caminho final deve ser:

```text
C:\src\flutter\bin\flutter.bat
```

Se você já extraiu e ficou `C:\src\flutter\flutter\bin`, corrija:

```powershell
Get-ChildItem "C:\src\flutter\flutter" -Force | Move-Item -Destination "C:\src\flutter" -Force
Remove-Item "C:\src\flutter\flutter" -Recurse -Force
```

> Não instale em `C:\Program Files`, em pastas com espaços/acentos ou dentro do
> OneDrive. Isso evita erros de permissão e de sincronização.

### Alternativa: script pronto

O script `instalar-flutter-3.47.7.ps1` (nesta pasta) faz o download (se
preciso), a extração, o PATH e o teste de versão.

**Se o Windows bloquear o `.ps1` por política de execução**, use o `.bat`
(duplo-clique), que chama o PowerShell com `-ExecutionPolicy Bypass`:

```text
instalar-flutter-3.47.7.bat
```

Se o `.bat` também foi bloqueado por ter vindo da rede, rode antes:
`Unblock-File .\instalar-flutter-3.47.7.bat`.

Ou rode pelo PowerShell:

```powershell
Unblock-File .\instalar-flutter-3.47.7.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\instalar-flutter-3.47.7.ps1
```

Se o zip estiver em outro lugar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\instalar-flutter-3.47.7.ps1 -Zip "D:\Downloads\flutter_windows_3.47.7-stable.zip"
```

Se uma política de grupo (GPO) bloquear até o `Bypass`, use os comandos
manuais do **TL;DR**: eles não dependem de arquivo `.ps1`.

### Alternativa por Git

```powershell
git clone https://github.com/flutter/flutter.git -b 3.47.7 C:\src\flutter
```

---

## 4. Colocar o Flutter no PATH

### Opção A — pela interface

1. Pressione `Win + R`, digite `sysdm.cpl` e dê Enter.
2. Aba **Avançado** → **Variáveis de Ambiente**.
3. Em **Variáveis do usuário**, selecione **Path** → **Editar**.
4. Clique em **Novo** e cole:

```text
C:\src\flutter\bin
```

5. Confirme com **OK** em todas as janelas.

### Opção B — pelo PowerShell

```powershell
$bin = "C:\src\flutter\bin"
$p = [Environment]::GetEnvironmentVariable("Path", "User")
$partes = ($p -split ';') | Where-Object { $_ -and ($_ -ne $bin) }
[Environment]::SetEnvironmentVariable("Path", "$bin;" + ($partes -join ';'), "User")
```

Isso coloca o Flutter novo **na frente** de qualquer instalação antiga. Se já
existir outro Flutter no PATH, `where.exe flutter` deve mostrar
`C:\src\flutter\bin\flutter.bat` primeiro.

**Feche e abra o PowerShell** depois de alterar o PATH.

Confira se o comando é encontrado:

```powershell
where.exe flutter
```

Deve aparecer `C:\src\flutter\bin\flutter.bat`.

---

## 5. Testar a instalação

```powershell
flutter --version
flutter doctor
```

Na primeira vez, o Flutter baixa o Dart SDK e alguns componentes. Pode levar
alguns minutos; precisa de internet.

O importante é que `flutter --version` mostre a versão do Flutter e do Dart.

---

## 6. Criar e testar um app de exemplo

```powershell
cd C:\src
flutter create meu_app
cd meu_app
flutter test
```

O resultado final deve ser parecido com:

```text
All tests passed!
```

Isso já prova que o SDK, o Dart e o toolchain de teste estão funcionando,
sem precisar de emulador Android.

### Ver o app rodando no navegador (opcional)

Precisa do **Google Chrome** instalado:

```powershell
flutter run -d chrome
```

Para gerar a versão web sem abrir o navegador:

```powershell
flutter build web
```

---

## 7. O que é normal no `flutter doctor`

- **Android toolchain com X**: normal se você não vai usar Android agora.
- **Android Studio não instalado**: normal; este guia não usa Android Studio.
- **Visual Studio com X**: normal se você não vai criar app para Windows desktop.
- **Chrome com X**: instale o Chrome se quiser testar no navegador.

Para este teste, ignore os avisos de Android/Visual Studio. O `flutter doctor`
pode continuar mostrando X nesses itens sem impedir o Flutter de funcionar.

Não rode `flutter doctor --android-licenses` agora: isso é só para Android.

---

## 8. Problemas comuns

| Problema | Solução |
|---|---|
| `flutter` não é reconhecido | Confira o PATH (`C:\src\flutter\bin`) e **abra um terminal novo**. |
| `where.exe flutter` não acha | O caminho está errado ou o zip foi extraído em pasta a mais. |
| `where.exe flutter` mostra outro caminho antes | Há outro Flutter no PATH. Use o comando que coloca `C:\src\flutter\bin` na frente ou remova a entrada antiga. |
| `flutter doctor` demora/trava na primeira vez | Está baixando componentes. Aguarde e confira a internet. |
| `git` não encontrado | Instale o Git (passo 2) e reabra o terminal. |
| Erro de permissão ao criar o app | Use `%USERPROFILE%\src` em vez de `C:\src`. |
| Antivírus muito lento no primeiro build | Adicione a pasta do projeto e `C:\src\flutter` às exclusões. |
| `cmdline-tools component is missing` | Só importa para Android; ignore neste guia. |
| `flutter test` falha por falta de dispositivo | `flutter test` não usa dispositivo. Confira se está dentro da pasta do app. |

---

## 9. Atualizar ou remover

Atualizar o Flutter (precisa de Git):

```powershell
flutter upgrade
flutter doctor
```

Para remover:

1. Apague a pasta `C:\src\flutter`.
2. Remova `C:\src\flutter\bin` do **Path** do usuário.
3. Apague os projetos de teste (`C:\src\meu_app`, etc.).

---

## 10. Checklist final

- [ ] `git --version` funciona
- [ ] `where.exe flutter` aponta para `C:\src\flutter\bin\flutter.bat`
- [ ] `flutter --version` mostra Flutter + Dart
- [ ] `flutter doctor` executa (avisos de Android/Visual Studio são normais)
- [ ] `flutter create meu_app` criou o projeto
- [ ] `flutter test` terminou com `All tests passed!`

Se todos os itens acima passarem, a instalação do Flutter está concluída.

# Instalando somente as Android SDK Tools no Windows (guia para Flutter)

> Antes deste guia, instale e teste o Flutter com
> `flutter-instalar-e-testar.md`. Este documento cobre só o Android SDK/emulador.

Objetivo: usar emulador Android com Flutter **sem** instalar o Android Studio completo.

> Validado no Windows 11 (24H2), Flutter 3.47.7 stable, JDK Temurin 17.
> Funciona em qualquer Windows 10/11 — o guia é **portátil**: nada de caminho ou
> usuário fixo, e o script detecta JDK/SDK existentes antes de instalar qualquer coisa.

---

##TL;DR — o script faz tudo

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-android-sdk.ps1
```

Variantes:

```powershell
# API 35 + emulador já iniciado
powershell -ExecutionPolicy Bypass -File .\setup-android-sdk.ps1 -ApiLevel 35 -Launch

# outro nome de AVD
powershell -ExecutionPolicy Bypass -File .\setup-android-sdk.ps1 -AvdName "pixel_8_api_35"
```

O script: detecta/instala o JDK 17, detecta o SDK existente, baixa as Command-line Tools
(build atual consultado no repositório do Google), aceita licenças, instala os pacotes,
registra `ANDROID_HOME`/`JAVA_HOME`/`PATH`, aponta o Flutter e cria o AVD.

---

## 0. O que muda de máquina para máquina

| Item | Onde o valor é resolvido |
|---|---|
| Usuário / pasta do SDK | `%LOCALAPPDATA%\Android\Sdk` (detectado automaticamente; outros caminhos são respeitados) |
| Versão do JDK | Detectada via `JAVA_HOME` → pastas do Temurin/Java/Microsoft → `java` no PATH |
| Build do ZIP das Tools | Consultado em `dl.google.com/android/repository/repository2-3.xml` (fallback: build fixo) |
| Nível de API | Parâmetro `-ApiLevel` (padrão 34) |
| SDK já instalado (Android Studio) | Reaproveitado — o script não reinstala nada |

Requisitos: Windows 10/11, Flutter stable, ~5 GB livres, Hyper-V/Windows Hypervisor Platform
habilitado (para o emulador).

---

## 1. Pré-requisitos

Instalar o JDK 17 (Temurin) via winget:

```powershell
winget install EclipseAdoptium.Temurin.17.JDK -e --accept-package-agreements --accept-source-agreements
```

Verificar:

```powershell
java -version
```

> Se o `java` não for reconhecido, o JDK está instalado mas fora do PATH da sessão:
> feche e abra o terminal. O script do TL;DR resolve isso automaticamente.

Detectar um JDK já existente:

```powershell
$jh = [Environment]::GetEnvironmentVariable("JAVA_HOME","Machine")
if (-not $jh) { $jh = [Environment]::GetEnvironmentVariable("JAVA_HOME","User") }
if (-not $jh) {
    $jh = (Get-ChildItem "C:\Program Files\Eclipse Adoptium" -Directory -ErrorAction SilentlyContinue |
           Where-Object { Test-Path "$($_.FullName)\bin\java.exe" } |
           Sort-Object Name -Descending | Select-Object -First 1).FullName
}
$jh
```

---

## 2. Definir o local do SDK

Padrão (portável, sem hardcode):

```powershell
$Sdk = "$env:LOCALAPPDATA\Android\Sdk"
New-Item -ItemType Directory -Path "$Sdk\cmdline-tools\latest" -Force
```

> O SDK ficará em `C:\Users\<seu-usuário>\AppData\Local\Android\Sdk`.
> Se já existir um SDK em outro lugar (ex.: Android Studio), use-o:
> `$Sdk = "C:\Android\Sdk"` ou aponte para o `ANDROID_HOME` já configurado.

Detectar um SDK já instalado:

```powershell
@(
  [Environment]::GetEnvironmentVariable("ANDROID_HOME","User"),
  [Environment]::GetEnvironmentVariable("ANDROID_HOME","Machine"),
  "$env:LOCALAPPDATA\Android\Sdk",
  "$env:USERPROFILE\AppData\Local\Android\Sdk",
  "C:\Android\Sdk"
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
```

---

## 3. Baixar as Command-line Tools

- Página oficial: <https://developer.android.com/studio#command-line-tools-only>
  (seção **"Command line tools only"**, aba **Windows**)
- Link direto do repositório Google:
  <https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip>

> O número do build muda com o tempo — pegue o valor atual na página oficial,
> ou consulte o repositório programaticamente:
>
> ```powershell
> $xml = (Invoke-WebRequest "https://dl.google.com/android/repository/repository2-3.xml" -UseBasicParsing).Content
> if ($xml -match 'commandlinetools-win-(\d+)_latest\.zip') { $build = $Matches[1] }
> $url = "https://dl.google.com/android/repository/commandlinetools-win-$build`_latest.zip"
> Invoke-WebRequest $url -OutFile "$env:TEMP\cmdline-tools.zip" -UseBasicParsing
> ```

---

## 4. Extrair na estrutura correta

> ⚠️ Erro mais comum: o ZIP precisa ser extraído **dentro** de `cmdline-tools\latest`,
> de forma que exista `latest\bin\sdkmanager.bat`.

```powershell
$Sdk = "$env:LOCALAPPDATA\Android\Sdk"
Expand-Archive -Path "$env:TEMP\cmdline-tools.zip" -DestinationPath "$env:TEMP\cmdt" -Force
Copy-Item "$env:TEMP\cmdt\cmdline-tools\*" "$Sdk\cmdline-tools\latest\" -Recurse -Force
```

Validar:

```powershell
Test-Path "$Sdk\cmdline-tools\latest\bin\sdkmanager.bat"   # deve retornar True
```

**Se retornar `False`:** a variável `$Sdk` está vazia no shell atual (aí o caminho vira
`\cmdline-tools\latest\...`, inexistente). Defina `$Sdk` antes e repita, ou use o caminho
completo. Sem variável, o teste correto é:

```powershell
Test-Path "$env:LOCALAPPDATA\Android\Sdk\cmdline-tools\latest\bin\sdkmanager.bat"
```

Conferir o que chegou ao destino:

```powershell
Get-ChildItem "$Sdk\cmdline-tools\latest"
# esperado: bin, lib, NOTICE.txt, source.properties
```

---

## 5. Registrar o SDK e o Java no ambiente

```powershell
$Sdk = "$env:LOCALAPPDATA\Android\Sdk"

[Environment]::SetEnvironmentVariable("ANDROID_HOME", $Sdk, "User")
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", $Sdk, "User")

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;$Sdk\cmdline-tools\latest\bin;$Sdk\platform-tools;$Sdk\emulator", "User")
```

JAVA_HOME (escopo `User` — não exige admin; use `Machine` só se souber o que está fazendo):

```powershell
$JavaHome = (Get-ChildItem "C:\Program Files\Eclipse Adoptium" -Directory |
             Where-Object { Test-Path "$($_.FullName)\bin\java.exe" } |
             Sort-Object Name -Descending | Select-Object -First 1).FullName
[Environment]::SetEnvironmentVariable("JAVA_HOME", $JavaHome, "User")
```

> Feche e reabra o terminal (ou o VS Code) para as mudanças valerem.

---

## 6. Aceitar as licenças

```powershell
$Sdk = "$env:LOCALAPPDATA\Android\Sdk"
(1..30 | ForEach-Object { "y" }) | & "$Sdk\cmdline-tools\latest\bin\sdkmanager.bat" --sdk_root="$Sdk" --licenses
```

Resultado esperado: `All SDK package licenses accepted`

Alternativa, depois do passo 8: `flutter doctor --android-licenses`

---

## 7. Instalar os componentes essenciais

```powershell
& "$Sdk\cmdline-tools\latest\bin\sdkmanager.bat" --sdk_root="$Sdk" `
  "platform-tools" `
  "emulator" `
  "platforms;android-34" `
  "build-tools;34.0.0" `
  "system-images;android-34;google_apis;x86_64"
```

Se a versão do build-tools/pacote não existir na sua máquina (as versões mudam com o tempo),
veja as disponíveis e ajuste:

```powershell
& "$Sdk\cmdline-tools\latest\bin\sdkmanager.bat" --sdk_root="$Sdk" --list
& "$Sdk\cmdline-tools\latest\bin\sdkmanager.bat" --sdk_root="$Sdk" --list_installed
```

Sugestões: `platforms;android-36` + `build-tools;36.0.0` (mais recente), ou
`platforms;android-34` + `build-tools;34.0.0` (compatível com AVDs API 33/34).

---

## 8. Apontar o Flutter para o SDK

```powershell
flutter config --android-sdk "$Sdk"
flutter doctor -v
```

Esperado:

```
[✓] Android toolchain - develop for Android devices (Android SDK version 36.0.0)
    • Android SDK at C:\Users\<user>\AppData\Local\Android\Sdk
    • Emulator version 37.x.x
    • Platform android-36, build-tools 36.0.0
```

---

## 9. Criar o AVD (emulador)

```powershell
"no" | & "$Sdk\cmdline-tools\latest\bin\avdmanager.bat" create avd `
  -n pixel_6_api_33 `
  -k "system-images;android-34;google_apis;x86_64" `
  --device "pixel_6" --force
```

Confirmar:

```powershell
& "$Sdk\cmdline-tools\latest\bin\avdmanager.bat" list avd
```

> Aceleração de hardware: habilite **Hyper-V** + **Windows Hypervisor Platform**
> em "Ativar ou desativar recursos do Windows" e a virtualização na BIOS/UEFI.
> Verifique com: `& "$Sdk\emulator\emulator.exe" -accel-check`
> Esperado: `WHPX(10.0.xxxxx) is installed and usable.`
> (sem isso o emulador não abre ou fica muito lento)

---

## 10. Rodar o emulador

```powershell
flutter emulators
flutter emulators --launch pixel_6_api_33
```

Ou diretamente:

```powershell
& "$Sdk\emulator\emulator.exe" -avd pixel_6_api_33
```

Em outro terminal:

```powershell
flutter devices
flutter run
```

---

## 11. Troubleshooting

| Sintoma | Solução |
|---|---|
| `Unable to locate Android SDK` | `flutter config --android-sdk "$Sdk"` e reabra o terminal |
| `java` não reconhecido | Reabra o terminal; se persistir, defina `JAVA_HOME` (passo 5) |
| `Test-Path` retorna `False` mesmo com o SDK instalado | `$Sdk` vazia no shell → defina a variável ou use `$env:LOCALAPPDATA\Android\Sdk` |
| `Move-Item/Copy-Item : Parte do caminho não foi encontrado` | `$Sdk` vazia no shell → use o caminho completo (passo 4) |
| `sdkmanager` não é reconhecido | ZIP extraído em nível errado → refaça o passo 4 |
| `flutter emulators` retorna vazio | Nenhum AVD criado ou falta `system-images` (passos 7 e 9) |
| Emulador não abre / erro de hypervisor | Ative Hyper-V e Windows Hypervisor Platform; habilite virtualização na BIOS |
| PowerShell bloqueia o `.bat` | Use `cmd.exe` ou `Set-ExecutionPolicy -Scope Process Bypass` |
| Flutter não acha o SDK após configurar | Feche e reabra o terminal/VS Code (env vars são lidas na inicialização) |
| `winget` não existe | Baixe o JDK manualmente em <https://adoptium.net> e continue do passo 5 |

---

## 12. Comandos úteis

```powershell
sdkmanager --list                    # pacotes disponíveis
sdkmanager --uninstall "emulator"    # remover pacote
avdmanager list avd                  # AVDs criados
adb devices                          # dispositivos conectados
flutter devices                      # dispositivos vistos pelo Flutter
emulator -list-avds                  # AVDs do emulador
emulator -accel-check                # status da aceleração (WHPX/Hyper-V)
```

---

## Apêndice — Desinstalar / reiniciar do zero

```powershell
flutter config --android-sdk ""      # remove a referência do Flutter
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\Android\Sdk"
Remove-Item -Recurse -Force "$env:USERPROFILE\.android\avd"
```

Para desinstalar componentes específicos, use `sdkmanager --uninstall "<pacote>"`.

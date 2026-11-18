# Criando apps Flutter: um para Android e outro para Web

> Para apenas **baixar, instalar e testar** o Flutter, use o guia curto
> `flutter-instalar-e-testar.md`. Este documento assume o Flutter já instalado.

Tutorial em duas partes, com todos os comandos **validados de ponta a ponta** nesta máquina:

- **Parte 1 — App Android**: `flutter create` → emulador → APK debug/release → App Bundle
- **Parte 2 — App Web**: `flutter create` → Chrome → `build/web` → publicação

> Pré-requisito da Parte 1: as Android SDK Tools já instaladas.
> Veja `android-sdk-tools-flutter.md` e o script `setup-android-sdk.ps1`.

App de exemplo usado e testado: `C:\Local\dev\exemplos\meu_app`
(mostra `Rodando em: Android` no emulador e `Rodando em: Web (Chrome)` no navegador).

---

# Parte 1 — App para Android

## 1.1 Criar o projeto

```powershell
cd C:\Local\dev\exemplos
flutter create --platforms=android --org br.com.exemplo --project-name meu_app meu_app
```

| Parâmetro | Para quê |
|---|---|
| `--platforms=android` | Só gera a pasta `android/` (sem web/ios/linux/windows) |
| `--org br.com.exemplo` | Prefixo do `applicationId` → `br.com.exemplo.meu_app` |
| `--project-name` | Nome do pacote Dart (sem hífen, sem espaços) |

Para gerar todas as plataformas: `flutter create meu_app` (sem `--platforms`).

Estrutura gerada:

```
meu_app/
├── lib/main.dart          # código Dart (o mesmo para Android e Web)
├── android/               # projeto Gradle nativo
│   ├── app/build.gradle.kts
│   └── app/src/main/AndroidManifest.xml
├── web/                   # index.html, manifest.json, ícones
├── test/                  # testes
├── pubspec.yaml           # dependências
└── analysis_options.yaml  # lint
```

## 1.2 O código do app (`lib/main.dart`)

Funciona igual no Android e na Web — usa `kIsWeb` do `foundation` para diferenciar:

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MeuApp());
}

class MeuApp extends StatelessWidget {
  const MeuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meu App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _counter = 0;
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final alvo = kIsWeb ? 'Web (Chrome)' : 'Android';
    return Scaffold(
      appBar: AppBar(title: const Text('Meu App')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Rodando em: $alvo',
                style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            Text('Valor do contador: $_counter',
                style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 16),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32),
              child: TextField(
                controller: _controller,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Seu nome',
                ),
              ),
            ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () {
                setState(() => _counter++);
                final nome = _controller.text.trim();
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Olá, ${nome.isEmpty ? 'mundo' : nome}!')),
                );
              },
              child: const Text('Incrementar'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 1.3 Rodar no emulador

```powershell
# 1. ligar o emulador
flutter emulators --launch pixel_6_api_33

# 2. conferir os dispositivos
flutter devices

# 3. rodar o app
flutter run
```

Comandos dentro do `flutter run` (console do Flutter):

| Tecla | Ação |
|---|---|
| `r` | hot reload (mantém o estado) |
| `R` | hot restart (reinicia o app) |
| `p` | mostra as widgets na árvore |
| `o` | alterna entre Android/iOS/web |
| `q` | encerra |

Escolher o dispositivo explicitamente:

```powershell
flutter run -d emulator-5554
flutter run -d chrome
```

## 1.4 Rodar em um celular físico (USB)

1. No celular: **Opções do desenvolvedor** → **Depuração USB** (ativar)
2. Conectar no USB e aceitar a chave RSA no aparelho
3. Conferir:

```powershell
adb devices
# List of devices attached
# XXXXXXXX    device
```

4. Rodar:

```powershell
flutter run -d XXXXXXXX
```

> Se a lista vier vazia, troque o cabo (precisa ser de dados), instale o driver USB do
> fabricante ou habilite **MTP**.

## 1.5 Gerar o APK

```powershell
cd C:\Local\dev\exemplos\meu_app

# debug (para testar)
flutter build apk --debug

# release (otimizado, para distributing)
flutter build apk --release

# um APK por arquitetura (menor download)
flutter build apk --release --split-per-abi

# App Bundle para a Play Store
flutter build appbundle --release
```

Saídas:

| Comando | Arquivo gerado |
|---|---|
| `build apk --debug` | `build/app/outputs/flutter-apk/app-debug.apk` |
| `build apk --release` | `build/app/outputs/flutter-apk/app-release.apk` |
| `build apk --release --split-per-abi` | `app-armeabi-v7a-release.apk`, `app-arm64-v8a-release.apk`, `app-x86_64-release.apk` |
| `build appbundle --release` | `build/app/outputs/bundle/release/app-release.aab` |

Instalar o APK manualmente no dispositivo/emulador:

```powershell
adb install -r build\app\outputs\flutter-apk\app-debug.apk
```

Abrir o app instalado:

```powershell
adb shell am start -n br.com.exemplo.meu_app/.MainActivity
```

## 1.6 Assinatura para release (Play Store)

1. Gerar keystore:

```powershell
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

2. Criar `android/key.properties` (não versionar no Git):

```properties
storePassword=SUA_SENHA
keyPassword=SUA_SENHA
keyAlias=upload
storeFile=/caminho/ate/upload-keystore.jks
```

3. Referenciar em `android/app/build.gradle.kts`:

```kotlin
val keystoreProperties = java.util.Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(keystorePropertiesFile.inputStream())
}

android {
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    buildTypes {
        release { signingConfig = signingConfigs.getByName("release") }
    }
}
```

## 1.7 Logs e diagnóstico

```powershell
flutter logs                    # log do app em execução
adb logcat                      # log do sistema
adb logcat | Select-String "flutter"
flutter doctor -v              # estado completo do toolchain
```

## 1.8 Problemas comuns (Android)

| Sintoma | Solução |
|---|---|
| `Unable to locate Android SDK` | `flutter config --android-sdk "$env:LOCALAPPDATA\Android\Sdk"` |
| Gradle para com erro de licença | `flutter doctor --android-licenses` e aceite tudo |
| `No connected devices` | `adb devices`; habilite depuração USB; `flutter emulators --launch <id>` |
| Emulador muito lento | Ative Hyper-V + Windows Hypervisor Platform; `emulator -accel-check` |
| `Failed to install the APK` | `adb uninstall br.com.exemplo.meu_app` e rode de novo |
| Erro de NDK/CMake | `flutter clean` e rebuild; deixe o Gradle baixar as ferramentas |
| Build lento na 1ª vez | Normal: baixa Gradle + NDK + SDK (pode levar 5–10 min) |

Limpeza quando algo "gruda":

```powershell
flutter clean
flutter pub get
```

---

# Parte 2 — App para Web

## 2.1 Criar o projeto

```powershell
cd C:\Local\dev\exemplos
flutter create --platforms=web --project-name meu_app_web meu_app_web
```

> O mesmo código Dart roda nas duas plataformas. Se quiser **um** projeto com as duas,
> use `--platforms=android,web` (como o exemplo `meu_app`).

## 2.2 Rodar no Chrome

```powershell
cd C:\Local\dev\exemplos\meu_app
flutter run -d chrome
```

- Abre o Chrome com o app em `http://localhost:<porta>`
- Hot reload funciona igual (`r` no console do Flutter)
- Para parar: `q`

Outros navegadores/dispositivos:

```powershell
flutter run -d edge          # Microsoft Edge
flutter run -d web-server    # só servidor (http://localhost:8080), abre no seu browser
```

## 2.3 Build de produção

```powershell
flutter build web --release
```

Saída em `build/web/`:

```
build/web/
├── index.html            # página inicial
├── main.dart.js          # bundle da aplicação
├── flutter.js
├── flutter_bootstrap.js
├── flutter_service_worker.js
├── manifest.json         # nome, ícones, cores (PWA)
├── favicon.png
├── assets/  canvaskit/  icons/
```

O `build/web` é **estático**: basta um servidor HTTP (sem backend) para servir.

Testar localmente antes de publicar:

```powershell
cd C:\Local\dev\exemplos\meu_app\build\web
python -m http.server 8099 --bind 127.0.0.1
# abrir http://127.0.0.1:8099/
```

> ⚠️ Abrir o `index.html` com `file://` **não funciona** (módulos ES e CORS).
> Use sempre um servidor HTTP.

## 2.4 Publicar

### Netlify (mais simples)

```powershell
npm i -g netlify-cli
netlify deploy --dir=build/web --prod
```

Ou pelo painel: arraste a pasta `build/web` em <https://app.netlify.com/drop>.

### Vercel

```powershell
npm i -g vercel
vercel --prod build/web
```

### GitHub Pages

```powershell
flutter build web --release --base-href "/meu-repo/"

cd build/web
git init
git add .
git commit -m "deploy"
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

No repositório: **Settings → Pages → Source: `main` / `root` / `/docs`** e copie
`build/web` para a pasta `docs`.

> Lembre de rebuildar com `--base-href` sempre que publicar em subpasta.

### Firebase Hosting

```powershell
npm i -g firebase-tools
firebase login
firebase init hosting     # public: build/web
firebase deploy
```

### Qualquer servidor / S3

Copie o conteúdo de `build/web` para o document root. Configure **fallback 404 → index.html**
(para rotas do SPA) e `Cache-Control` longo para `*.js` / `canvaskit/`.

## 2.5 Personalizar a página web

- `web/index.html` — título `<title>`, `<meta name="description">`, fonte, cor de fundo
- `web/manifest.json` — nome do app, `short_name`, `theme_color`, ícones
- `web/favicon.png` — ícone da aba
- Ícones PWA: `web/icons/Icon-192.png`, `Icon-512.png`, `Icon-maskable-192.png`, `Icon-maskable-512.png`

Trocar a cor da barra do navegador:

```html
<meta name="theme-color" content="#3F51B5">
```

## 2.6 Opções de build

```powershell
flutter build web --release --wasm                 # compila para WebAssembly
flutter build web --release --no-tree-shake-icons  # mantém todos os ícones
flutter build web --release --base-href "/sub/"    # deploy em subpasta
flutter build web --profile --dart-define=API_URL=https://api.exemplo.com
flutter build web --wasm --release                 # produção com Wasm
```

Variáveis de ambiente por plataforma:

```dart
const String apiUrl = String.fromEnvironment('API_URL', defaultValue: 'http://localhost:3000');
```

```powershell
flutter run -d chrome --dart-define=API_URL=https://api.exemplo.com
```

## 2.7 Limitações da Web

- **Sem `dart:io`** (leitura de arquivos, sockets, processos) — use packages web
  (`http`, `shared_preferences`, `url_launcher` têm suporte web)
- **Plugins sem suporte web**: confira em <https://pub.dev/packages> (ícone de plataforma web)
- **Sem acesso ao sistema de arquivos** do usuário (apenas download/upload via File API)
- **Renderização em canvas**: o texto não fica no HTML → SEO ruim e leitores de tela
  precisam da camada de semântica (o Flutter ativa o *semantics tree* sob demanda)
- **Push notification** e **sensores** dependem do suporte do navegador

## 2.8 Problemas comuns (Web)

| Sintoma | Solução |
|---|---|
| Página em branco | Serviu por `file://` → use servidor HTTP; veja o console do navegador |
| Erro de CORS no console | Recarregue com `flutter run` (o Dev Server já envia os headers certos) |
| App serve versão velha | Limpe o cache do service worker: DevTools → Application → Clear storage |
| Não encontra `flutter_bootstrap.js` | Build incompleto → rode `flutter build web --release` de novo |
| Imagens/fontes sumiram | Caminho relativo em subpasta → use `--base-href` |
| Erro `wasm` no build | Versão antiga do Dart → atualize o Flutter (`flutter upgrade`) |
| `setState() called after dispose()` | Guarde o `TextEditingController` e chame `dispose()` (como no exemplo) |

---

# Comandos resumidos

```powershell
# projeto
flutter create --platforms=android,web --org br.com.exemplo meu_app
cd meu_app
flutter pub get
flutter pub add http

# rodar
flutter devices
flutter run
flutter run -d emulator-5554
flutter run -d chrome

# build
flutter build apk --release
flutter build appbundle --release
flutter build web --release

# limpar
flutter clean && flutter pub get
```

# Checklist de publicação

**Android**
- [ ] `flutter build appbundle --release` gerou o `.aab`
- [ ] Keystore configurada e guardada com segurança
- [ ] `applicationId`/versão corretos em `android/app/build.gradle.kts`
- [ ] Ícone e nome do app em `android/app/src/main/AndroidManifest.xml`
- [ ] APK testado em device real (`flutter install`)

**Web**
- [ ] `flutter build web --release` sem erros
- [ ] `build/web` servido por HTTP e testado
- [ ] `web/manifest.json`, `favicon.png` e `<title>` ajustados
- [ ] `--base-href` correto se published em subpasta
- [ ] Sem erros no console do navegador

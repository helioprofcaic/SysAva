# Tailscale — acesso remoto ao laboratório

Guia prático para acessar os PCs do laboratório **de qualquer lugar** (casa, 4G,
outra escola) sem DDNS, sem abrir portas no roteador e sem IP público fixo.

---

## 1. Em uma frase

O Tailscale dá a cada dispositivo da sua conta um **IP privado fixo `100.x`**
(e um nome), mesmo atrás de NAT. Um PC dentro do laboratório "empresta" a rede
local inteira para essa rede privada — e o seu notebook passa a enxergar os PCs
como se estivesse sentado lá.

---

## 2. O que é (e o que não é)

- **É um aplicativo** (Windows, macOS, Linux, Android, iOS). **Não é biblioteca
  Python** — não se importa nada no código. (Existe SDK para integrar, mas não é
  necessário aqui.)
- **É uma VPN em malha (mesh) sobre WireGuard.** Cada cliente abre um túnel
  criptografado. O serviço do Tailscale na nuvem (*control plane*) serve só para
  seus dispositivos se encontrarem (troca de chaves/endereços), não para
  transportar seus dados.
- **"Online" pode significar duas coisas:**
  - precisa de **internet** para o login/descoberta (e para o relay quando o
    NAT impede conexão direta);
  - mas o tráfego, quando possível, vai **direto de um dispositivo para o
    outro** (ponto a ponto), sem passar pelos servidores do Tailscale.
- **Não é DDNS:** DDNS responde "qual é o IP público da escola?"; o Tailscale
  responde "você está dentro da rede da escola" — sem depender de IP público.
- **Não abre portas** no roteador e **não expõe** o laboratório para a internet.
  Só dispositivos da **sua conta** (tailnet) entram.

---

## 3. Conceitos que aparecem no caminho

| Termo | O que é |
| --- | --- |
| **Tailnet** | A sua rede privada (a conta onde os dispositivos entram). |
| **IP `100.x`** | Endereço privado fixo que cada dispositivo recebe (faixa CGNAT). |
| **MagicDNS** | Nome automático de cada máquina, ex.: `pc01-lab02.<tailnet>.ts.net`. |
| **Subnet router** | Um dispositivo que anuncia uma **sub-rede** (ex.: `192.168.10.0/23`) para o tailnet. |
| **accept-routes** | No cliente que quer usar as rotas anunciadas (o notebook). |
| **DERP** | Relay do Tailscale usado quando o NAT impede conexão direta (mais lento, mas funciona). |
| **Exit node** | Fazer todo o tráfego de internet sair por outro PC. **Não precisamos** disso. |

### Diagrama do seu caso

```
[Casa / 4G]
 Notebook  100.121.243.21
        │  túnel WireGuard (criptografado)
        ▼
 PC01-LAB02  100.x.y.z   (Tailscale + subnet router)
        │  rede local normal do laboratório
        ├── PC02  192.168.10.13
        ├── PC03  192.168.11.225
        ├── PC04  192.168.10.70
        └── ... (todos os PCs, sem Tailscale instalado)
```

Só o **PC01** precisa do Tailscale. Os demais são alcançados **através** dele,
pelo IP `192.168.x` de sempre. É isso que substitui o DDNS.

---

## 4. Passo a passo (uma vez)

### 4.1 Conta

1. Crie/entre em <https://login.tailscale.com> (pode usar Google/Microsoft).
2. Plano gratuito cobre o laboratório (até 100 dispositivos).
3. **Use a conta institucional (Gmail da escola) nos dois dispositivos** — o
   tailnet é por conta; notebook e PC01 precisam estar na mesma. Se o Google
   Workspace bloquear apps de terceiros, a TI precisa liberar o Tailscale.
   Para o post no fórum (Aula 01 de DevOps), use
   `docs/FORUM_AULA01_DEVOPS_TAILSCALE.md`.

### 4.2 Notebook (lado de fora)

1. Se ainda não tiver: instale de <https://tailscale.com/download/windows>
   (ou `winget install --id Tailscale.Tailscale`).
2. Faça login **na mesma conta**.
3. Confira:
   ```powershell
   tailscale status
   tailscale ip -4
   ```

### 4.3 PC01-LAB02 (o "porteiro" dentro da escola)

1. Instale o Tailscale (precisa de Administrador) e faça login **na mesma
   conta**.
2. Descubra a sub-rede do laboratório:
   ```powershell
   Get-NetIPConfiguration | Select-Object InterfaceAlias, IPv4Address, IPv4DefaultGateway
   ```
   No seu caso os PCs aparecem em `192.168.10.x` e `192.168.11.x` — a faixa
   `192.168.10.0/23` cobre os dois.
3. Anuncie a sub-rede (PowerShell como Administrador):
   ```powershell
   tailscale up --advertise-routes=192.168.10.0/23
   ```
   > Ajuste a faixa se a rede mudar. Se o laboratório usar só `192.168.10.x`,
   > use `192.168.10.0/24`.
4. No painel do Tailscale: <https://login.tailscale.com/admin/machines> →
   selecione **PC01-LAB02** → **Edit route settings** → marque
   `192.168.10.0/23` → **Save**. (Rota não aprovada = não funciona.)

### 4.4 Notebook: aceitar as rotas

O Windows às vezes já aceita; para garantir:

```powershell
tailscale up --accept-routes
```

### 4.5 Testar de fora

1. Desconecte o notebook do Wi-Fi da escola (use o celular como roteador).
2. Rode:
   ```powershell
   ping 192.168.11.246      # PC01 (exemplo)
   curl http://192.168.11.246:5000/health
   ```
3. Abra no navegador:
   - Painel do monitor: `http://192.168.11.246:5000/`
   - SysAva principal: `http://192.168.10.15:8501` (do notebook) ou a máquina
     onde ele roda.
4. Se respondeu, está pronto.

---

## 5. O que já funciona depois disso

- Painel do monitor (`:5000`) e o SysAva (`:8501`) de qualquer lugar.
- **RDP** nos PCs do laboratório (`mstsc /v:192.168.10.13`) — habilite o RDP no
  PC e libere no firewall, se ainda não estiver.
- **PowerShell remoting / SMB** para manutenção de arquivos.
- Os comandos do painel continuam iguais (o Tailscale só muda o caminho até o
  PC; o agente/lock não precisam de nada novo).

---

## 6. Segurança

- Só entra quem está na **sua tailnet** (a sua conta). Não há porta aberta para
  a internet.
- Remova dispositivos perdidos no admin; configure expiração de chave.
- Em *Access Controls* (ACLs) você pode limitar quem fala com quem, se um dia
  houver mais de um professor na conta.
- O Tailscale **não tem relação com a cota do Supabase** (não passa por ele).

---

## 7. Limitações e cuidados

- O **PC01 precisa estar ligado** para ser o porteiro. Se ele estiver desligado,
  use Wake-on-LAN (do próprio servidor, se houver outro PC ligado) ou instale o
  Tailscale nos PCs que precisar.
- O subnet router **no Windows** funciona, mas é menos maduro que no Linux. Se
  der problema, alternativas: instalar o Tailscale nos PCs do laboratório
  (admin, uma vez) ou usar um Raspberry Pi/Linux como porteiro.
- Se a escola mudar a faixa (repetidor/roteador novo), revise
  `--advertise-routes` e aprove de novo no admin.
- Se o notebook estiver na **mesma** rede do laboratório, o Tailscale nem é
  necessário — ele só é essencial de fora.
- `100.x` é para o Tailscale. Os IPs `192.168.x` continuam sendo os "de dentro".

---

## 8. Problemas comuns

| Sintoma | Causa provável | O que fazer |
| --- | --- | --- |
| `ping 192.168.x` não responde de fora | Rota não aprovada no admin | *Edit route settings* → marcar a sub-rede |
| Notebook vê o PC01 (`100.x`) mas não os outros PCs | Falta `--accept-routes` no notebook | `tailscale up --accept-routes` |
| Tudo lento | Conexão direta bloqueada (NAT) → DERP | Normal em algumas redes; testar em outra |
| PC01 aparece offline | PC desligado/sem internet | Ligar; conferir `tailscale status` |
| Deixou de funcionar após troca de roteador | Mudou a sub-rede | Ajustar `--advertise-routes` e aprovar |
| `tailscale: command not found` | App não instalado ou PATH | Reinstalar/abrir novo terminal |

---

## 9. e o inventário (`pc_registry`)?

O Tailscale é o **caminho** (como chegar). Ele **não** guarda
"quem é o PC, qual IP/MAC, qual aluno, qual versão do agente, último sinal" —
isso é o **registro** que propus no Supabase (`pc_registry`), lido pelo painel.
Os dois se completam:

- **Tailscale** → acesso (RDP, painel, PowerShell) de fora.
- **Supabase `pc_registry`** → inventário/histórico consultável de qualquer lugar.
- **Drive** → opcional, só um snapshot periódico do inventário (não a fonte viva).

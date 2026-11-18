# Aula 01 — DevOps: acesso remoto seguro ao laboratório com Tailscale

**Disciplina:** Introdução ao Ecossistema DevOps
**Aula:** 01
**Turma:** 2ª SÉRIE — Turma I-A (Técnico DS)
**Professor:** Helio P. Lima
**Tema:** rede privada, NAT, VPN e acesso remoto — na prática.

---

## 🎯 Objetivo

Permitir que o professor acesse **todos os PCs do laboratório** (painel do
monitor, RDP, PowerShell, arquivos) **de qualquer lugar** — casa, 4G, outra
escola — **sem DDNS, sem IP público fixo e sem abrir portas no roteador**.

Ferramenta: **Tailscale** (VPN em malha sobre WireGuard).

> Conta usada: **Gmail institucional** (a mesma nos dois computadores).
> Plano gratuito: até 100 dispositivos — suficiente para o laboratório.

---

## 🧠 Ideia em 30 segundos

- Cada dispositivo que entra na conta ganha um **IP privado fixo `100.x`**
  e um nome (MagicDNS), mesmo atrás do NAT.
- Um PC dentro do laboratório (**PC01-LAB02**) anuncia a **sub-rede local**
  (`192.168.10.0/23`) para a sua conta. Ele é o **porteiro**.
- O notebook, de fora, passa a enxergar os IPs `192.168.x` **como se estivesse
  sentado no laboratório**.
- O tráfego vai **criptografado direto** entre os dispositivos. O serviço do
  Tailscale só ajuda as pontas a se encontrarem.

```
Notebook (100.x)  ── túnel WireGuard ──  PC01-LAB02 (100.y)
                                              │
                                    rede local 192.168.10.0/23
                                    ├── PC02 192.168.10.13
                                    ├── PC03 192.168.11.225
                                    └── ...
```

**Por que não DDNS?** DDNS só descobre o IP público da escola; os IPs dos PCs
são privados e não são alcançáveis de fora sem um túnel. O Tailscale é o túnel
(com login e criptografia), e não expõe nada para a internet.

---

## ✅ Pré-requisitos

- [ ] Conta **Gmail institucional** (Google Workspace da escola).
- [ ] Acesso de **Administrador** no notebook e no PC01-LAB02.
- [ ] Internet nos dois (a rede do laboratório pode ser Wi-Fi ou cabo).
- [ ] Se o Workspace bloquear apps de terceiros, pedir à TI para **permitir o
      Tailscale** (ou usar um tailnet criado pela escola).

---

## 🖥️ Parte 1 — Notebook do professor

1. Instale (PowerShell como Administrador):
   ```powershell
   winget install --id Tailscale.Tailscale -e --accept-source-agreements --accept-package-agreements
   ```
   (ou baixe em <https://tailscale.com/download/windows>)

2. No ícone do Tailscale (bandeja) → **Log in** → escolha **Google** e entre com
   o **Gmail institucional**.

3. Confira o IP do notebook:
   ```powershell
   tailscale status
   tailscale ip -4
   ```
   Guarde o `100.x.y.z` — é o endereço “de fora” do notebook.

---

## 🏫 Parte 2 — PC01-LAB02 (o porteiro)

1. Instale igual (PowerShell como Administrador):
   ```powershell
   winget install --id Tailscale.Tailscale -e --accept-source-agreements --accept-package-agreements
   ```

2. **Marque “Run unattended”** (roda como serviço, mesmo antes do login/na tela
   de bloqueio). Se não aparecer, abra o Tailscale → *Preferences* → habilite
   *Run unattended*.

3. Faça login com **o mesmo Gmail institucional** usado no notebook.

4. Descubra a sub-rede do laboratório:
   ```powershell
   ipconfig
   ```
   Procure o adaptador em uso (Wi-Fi/Ethernet) e anote **IPv4** e **máscara**.
   Exemplo: `192.168.10.161` com máscara `255.255.254.0` = faixa
   `192.168.10.0/23` (cobre `192.168.10.x` **e** `192.168.11.x`).

5. Teste se ele alcança os PCs das duas faixas:
   ```powershell
   ping 192.168.10.13
   ping 192.168.11.225
   ```

6. Anuncie a sub-rede (PowerShell como Administrador):
   ```powershell
   tailscale up --advertise-routes=192.168.10.0/23
   ```
   > Ajuste a faixa conforme o `ipconfig`. Se o laboratório usa só
   > `192.168.10.x`, use `192.168.10.0/24`.

---

## 🔐 Parte 3 — Aprovar a rota (o passo que todo mundo esquece)

1. Abra <https://login.tailscale.com/admin/machines> no navegador.
2. Selecione **PC01-LAB02**.
3. **Edit route settings** → marque `192.168.10.0/23` → **Save**.
4. Na mesma tela, em **Key expiry**, clique em **Disable key expiry** para o
   PC01 (senão, em ~180 dias o acesso remoto para sozinho).

---

## 🔁 Parte 4 — Notebook: aceitar as rotas

```powershell
tailscale up --accept-routes
```

---

## 🧪 Parte 5 — Testar de fora

1. Desconecte o notebook do Wi-Fi da escola (use o **celular como roteador**).
2. Teste a conexão com o servidor do laboratório:
   ```powershell
   curl.exe http://192.168.11.246:5000/health
   ```
3. Abra no navegador:
   - Painel do monitor: `http://192.168.11.246:5000/`
   - SysAva principal: `http://192.168.10.15:8501`
4. Se abriu, está funcionando. 🎉

> Dica: na mesma rede do laboratório o Tailscale nem é necessário — ele é
> essencial **de fora**.

---

## 🛡️ Segurança

- Só entra quem está na **mesma conta** (tailnet). Nada de porta aberta na
  internet.
- Não compartilhe a conta; se um dispositivo for perdido, **remova** em
  *Machines*.
- Em *Access Controls* (ACLs) é possível limitar quem acessa o quê.
- O Tailscale **não** tem relação com a cota do Supabase — ele só cria o
  caminho de rede.

---

## 🧰 Problemas comuns

| Sintoma | Causa provável | Solução |
| --- | --- | --- |
| Notebook vê o PC01 (`100.x`), mas não os `192.168.x` | Rota não aprovada ou `--accept-routes` faltando | Aprovar no admin e rodar `tailscale up --accept-routes` |
| `ping` não responde de fora | PC01 desligado / sem internet | Ligar o PC01; conferir `tailscale status` |
| Funcionou e parou depois de trocar o roteador | Mudou a faixa da rede | Ajustar `--advertise-routes` e aprovar de novo |
| Deixou de funcionar após ~6 meses | Chave expirou | *Disable key expiry* no PC01 |
| `tailscale: command not found` | App não instalado / terminal antigo | Reinstalar e abrir um PowerShell novo |
| Login Google recusado | Workspace bloqueia app de terceiros | Pedir liberação à TI |

---

## 📋 Checklist final

- [ ] Tailscale instalado e logado no notebook (Gmail institucional)
- [ ] Tailscale instalado e logado no PC01 (**unattended**)
- [ ] Sub-rede conferida no `ipconfig`
- [ ] `tailscale up --advertise-routes=...` executado no PC01
- [ ] Rota **aprovada** no admin do Tailscale
- [ ] `tailscale up --accept-routes` no notebook
- [ ] Teste de fora (4G) acessando o painel `http://<ip-do-PC01>:5000/`
- [ ] *Disable key expiry* no PC01

---

## 🔗 Para saber mais

- Site: <https://tailscale.com>
- Subnet router: <https://tailscale.com/kb/1019/subnets>
- Guia interno do projeto: `docs/TAILSCALE.md`

> **Próximo passo (aula seguinte):** inventário dos PCs (`pc_registry` no
> Supabase) — IP, MAC, aluno, versão do agente e último sinal, consultável de
> qualquer lugar, com botão de Wake-on-LAN.

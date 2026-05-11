# Deploy do Dashboard — Streamlit Community Cloud

Guia passo-a-passo para publicar o dashboard de auditoria das OSS de Goiás.

---

## ⚠️ Antes de começar — decisão crítica

Streamlit Community Cloud **gratuito exige repositório PÚBLICO** no GitHub. Isso significa que **código E dados** ficam visíveis para qualquer pessoa.

Opções:

| Opção | Custo | Quem vê o código | Quem vê o dashboard |
|---|---|---|---|
| **A.** Streamlit Cloud + repo público | Grátis | 🌍 Todo mundo | 🌍 Todo mundo (com URL) |
| **B.** Streamlit Cloud + repo público + senha simples | Grátis | 🌍 Todo mundo | 🔒 Só quem tem a senha |
| **C.** Streamlit Cloud Teams + repo privado | ~US$ 250/mês | 🔒 Você | 🌍 Todo mundo (com URL) |
| **D.** Render (free tier) + repo privado | Grátis | 🔒 Você | 🌍 Todo mundo (com URL) |

**Recomendação para apresentação ao Governador:** Opção **B** — rápida, gratuita, código fica auditável (positivo para transparência), e dashboard tem barreira de acesso simples.

---

## Passo 1 — Preparar a chave secreta

Crie um arquivo local `.streamlit/secrets.toml` (já no `.gitignore` — não vai para o repo):

```toml
anthropic_api_key = "sk-ant-api03-…"
dashboard_password = "GovGO2026"   # opcional — vide passo 5
```

---

## Passo 2 — Criar repositório no GitHub

```bash
cd C:\OSS-Goias

git init
git add .
git commit -m "Dashboard de auditoria das OSS de Goiás"

# Cria o repo via GitHub CLI (instale antes: winget install GitHub.cli)
gh auth login
gh repo create oss-goias-dashboard --public --source=. --push
```

> **Não tem `gh` CLI?** Crie o repositório manualmente em github.com, depois:
> ```bash
> git remote add origin https://github.com/SEU-USUARIO/oss-goias-dashboard.git
> git branch -M main
> git push -u origin main
> ```

**Confira que o `.gitignore` está ativo:**

```bash
git status --ignored | findstr secrets.toml
git status --ignored | findstr .api-key
```

Esses dois arquivos DEVEM aparecer como ignorados. Se aparecerem como staged, **interrompa o commit**.

---

## Passo 3 — Conectar ao Streamlit Cloud

1. Acesse https://share.streamlit.io
2. Clique em **"New app"**
3. Conecte sua conta GitHub
4. Preencha:
   - **Repository:** `SEU-USUARIO/oss-goias-dashboard`
   - **Branch:** `main`
   - **Main file path:** `dashboard/app.py`
   - **App URL** (opcional): `oss-goias` → vira `https://oss-goias.streamlit.app`

---

## Passo 4 — Configurar secrets na nuvem

Ainda no painel do Streamlit Cloud, clique em **"Advanced settings"** antes de fazer deploy. Cole no campo **Secrets**:

```toml
anthropic_api_key = "sk-ant-api03-SUA-CHAVE-AQUI"
dashboard_password = "GovGO2026"
```

Salve. Em seguida clique **"Deploy"**. O build leva 2–4 min.

---

## Passo 5 — (Opcional, recomendado) Adicionar senha simples

Para a apresentação ao Governador, adicione um gate de senha. Edite `dashboard/app.py` adicionando no topo (depois dos imports, antes do `setup_page`):

```python
import streamlit as st

def _gate():
    pwd_required = st.secrets.get("dashboard_password")
    if not pwd_required:
        return  # sem senha configurada — acesso livre
    if st.session_state.get("auth_ok"):
        return
    st.set_page_config(page_title="OSS Goiás · Acesso", page_icon="🔒", layout="centered")
    st.markdown("# 🔒 Dashboard da Auditoria das OSS")
    st.caption("Acesso restrito · Secretaria de Estado da Saúde de Goiás")
    pwd = st.text_input("Senha de acesso", type="password")
    if pwd == pwd_required:
        st.session_state["auth_ok"] = True
        st.rerun()
    elif pwd:
        st.error("Senha incorreta.")
    st.stop()

_gate()
```

Faça commit e push — Streamlit Cloud redeploya automaticamente.

---

## Passo 6 — Validação pós-deploy

Acesse a URL pública e teste:

- [ ] Home carrega com hero verde e KPIs
- [ ] Navegação entre as 5 páginas funciona
- [ ] "Pergunte aos Dados" responde a uma pergunta de teste
- [ ] Gráficos renderizam (formato R$ pt-BR no eixo Y)
- [ ] Sidebar não mostra a chave em `Manage app → Logs`

---

## Rollback rápido

Se algo quebrar em produção:

```bash
git log --oneline -10                # encontra o último commit bom
git revert <hash-do-commit-quebrado>
git push
```

O Streamlit Cloud redeploya em ~1 min.

---

## Alternativas se Streamlit Cloud não servir

### Render (repo privado grátis)

```yaml
# render.yaml na raiz
services:
  - type: web
    name: oss-goias-dashboard
    runtime: python
    pythonVersion: "3.13"
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run dashboard/app.py --server.port $PORT --server.headless true --server.address 0.0.0.0
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false   # configurar manualmente no painel
```

Acesse render.com → New → Web Service → conecte o repo (pode ser privado).

### Túnel local (para apresentação única)

Se for **uma única reunião**, talvez nem precise deploy permanente. Rode local e exponha temporariamente:

```bash
# Terminal 1 — rode o dashboard
python -m streamlit run dashboard/app.py

# Terminal 2 — exponha publicamente via Cloudflare Tunnel (grátis, sem cadastro)
# Baixe cloudflared em https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
cloudflared tunnel --url http://localhost:8501
```

Cloudflare devolve uma URL `https://*.trycloudflare.com` válida pela duração da sessão. Zero infraestrutura, dados nunca saem da sua máquina.

---

## Custos esperados

| Item | Custo mensal |
|---|---|
| Streamlit Cloud (free) | R$ 0 |
| Domínio próprio (opcional) | ~R$ 40/ano via Registro.br |
| Chamadas Anthropic (Pergunte aos Dados) | ~R$ 0,10 por pergunta com cache; ~R$ 30/mês para uso moderado |

---

## Suporte

- **Logs do app:** painel Streamlit Cloud → **Manage app → Logs**
- **Reiniciar:** **Manage app → Reboot**
- **Limpar cache:** **Manage app → Clear cache** (útil se os CSVs mudarem)

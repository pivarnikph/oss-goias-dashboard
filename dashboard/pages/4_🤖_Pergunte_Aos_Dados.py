"""Pergunte aos Dados — chat com Claude que consulta os CSVs e responde com análise."""
import sys
import re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    setup_page, load_fato, load_outliers, load_categorias_gasto,
    load_producao_vs_meta, load_contratos, get_api_key, header,
    COLORS, fmt_brl, fmt_pct,
)

try:
    import anthropic
except ImportError:
    st.error("`anthropic` não instalado. Rode: `pip install anthropic`")
    st.stop()

setup_page("Pergunte aos Dados", "💬")
header(
    titulo="Pergunte aos Dados",
    subtitulo="Faça perguntas em português natural — a inteligência artificial consulta os dados e responde com gráficos, tabelas e análise.",
    pill="IA",
)

# ===== Setup API =====
api_key = get_api_key()
if not api_key:
    st.error("ANTHROPIC_API_KEY não configurada.")
    st.stop()
client = anthropic.Anthropic()

# ===== Dados =====
df_fato = load_fato()
df_out = load_outliers()
df_cat = load_categorias_gasto()
df_pvm = load_producao_vs_meta()
df_contr = load_contratos()

def build_data_summary():
    return f"""Você tem acesso aos seguintes DataFrames pandas:

## df_fato (tabela principal — 1 linha por hospital × ano × mês)
Linhas: {len(df_fato)} | Colunas: {list(df_fato.columns)}
Hospitais: {sorted(df_fato['hospital'].dropna().unique().tolist())}
OSS: {sorted(df_fato['oss'].dropna().unique().tolist())}
Período: {df_fato['ano_mes'].min()} a {df_fato['ano_mes'].max()}

Estatísticas-chave:
{df_fato[['recebidos_ses','executados','devolvidos','perc_exec_financeira','consultas','internacoes','custo_por_consulta','custo_por_internacao']].describe().round(2).to_string()}

## df_out (outliers já detectados)
Linhas: {len(df_out)} | Colunas: {list(df_out.columns)}

## df_cat (categorias de gasto detalhadas)
Linhas: {len(df_cat)} | Colunas: {list(df_cat.columns)}

## df_pvm (produção realizada vs meta — 1 linha por hospital × período × indicador)
Linhas: {len(df_pvm)} | Colunas: {list(df_pvm.columns)}

## df_contr (contratos de gestão)
Linhas: {len(df_contr)} | Colunas: {list(df_contr.columns)}
"""

DATA_SUMMARY = build_data_summary()

SYSTEM_PROMPT = f"""Você é um analista de dados especializado em auditoria de Organizações Sociais de Saúde (OSS) do Estado de Goiás. Você tem acesso a DataFrames pandas com dados financeiros, de produção e contratuais de hospitais públicos geridos por OSS.

Para responder à pergunta do usuário, gere código Python seguro usando pandas que processa os DataFrames disponíveis. Seu código deve:
1. Definir uma variável `resultado` com o DataFrame ou valor que responde a pergunta
2. Opcionalmente definir `figura` como um objeto plotly.graph_objects.Figure ou plotly.express.Figure para visualizar
3. Não usar I/O nem importar bibliotecas externas além de: pandas (pd), numpy (np), plotly.express (px), plotly.graph_objects (go)
4. Não modificar os DataFrames originais
5. Comentar o código brevemente

Quando criar uma figura plotly, use a paleta institucional do Estado de Goiás:
- Verde primário: {COLORS['verde']}
- Verde escuro: {COLORS['verde_dark']}
- Vermelho alerta: {COLORS['alerta']}
- Dourado: {COLORS['dourado']}
- Azul informação: {COLORS['info']}

Após gerar o código, escreva uma análise narrativa curta (2-4 frases) explicando o que o resultado significa.

Formato:
```python
# código aqui
resultado = ...
figura = ...  # opcional
```

**Análise:** [explicação narrativa]"""

# ===== Tip card =====
st.markdown(
    f"""<div class="tip-card" style="margin-bottom: 1.5rem;">
    <div class="tip-card-icon">💡</div>
    <p class="tip-card-text"><strong>Como funciona:</strong> escreva sua pergunta como faria a um colega. A IA traduz para uma consulta nos dados e devolve a resposta com gráfico, tabela e explicação. Quanto mais específica a pergunta, melhor a resposta.</p>
</div>""",
    unsafe_allow_html=True,
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== Sugestões em grade visual =====
if not st.session_state.messages:
    st.markdown(
        '<div class="section-label" style="margin-top: 1rem;">'
        '<h2 class="section-label-title" style="font-size: 1.0625rem;">Comece com uma sugestão</h2>'
        '<p class="section-label-hint">Clique para enviar diretamente</p></div>',
        unsafe_allow_html=True,
    )

    samples = [
        ("💰", "Devoluções baixas", "Quais hospitais devolveram menos de 1% do que receberam?"),
        ("📈", "Evolução de custo", "Mostre a evolução do custo por consulta em HUGOL ao longo do tempo"),
        ("⚖️", "Comparação OSS", "Compare AGIR e FUNEV em termos de execução financeira"),
        ("🏥", "Ocupação alta", "Existem hospitais com taxa de ocupação acima de 95%?"),
        ("📉", "Tendência negativa", "Quais OSS apresentam tendência de queda na execução em 2026?"),
        ("📋", "Grandes contratos", "Liste contratos com valor total acima de R$ 500 milhões"),
        ("🔍", "Sobrexecução", "Em quais meses HEANA gastou mais que recebeu?"),
        ("🔗", "Correlação", "Qual a correlação entre número de consultas e taxa de ocupação?"),
    ]
    cols = st.columns(2)
    for i, (icon, label, q) in enumerate(samples):
        col = cols[i % 2]
        with col:
            if st.button(f"{icon}  **{label}** — {q}", key=f"sample_{i}", use_container_width=True, type="secondary"):
                st.session_state.pending_question = q
                st.rerun()

# ===== Histórico do chat =====
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("dataframe") is not None:
            st.dataframe(msg["dataframe"], use_container_width=True)
        if msg.get("figure") is not None:
            st.plotly_chart(msg["figure"], use_container_width=True)
        if msg.get("code"):
            with st.expander("Ver código gerado"):
                st.code(msg["code"], language="python")

# ===== Input =====
prompt = st.chat_input("Pergunte algo sobre os dados...")
if "pending_question" in st.session_state:
    prompt = st.session_state.pending_question
    del st.session_state.pending_question

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando os dados…"):
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=2000,
                    system=[{
                        "type": "text",
                        "text": SYSTEM_PROMPT + "\n\n" + DATA_SUMMARY,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text
            except Exception as e:
                st.error(f"Erro ao consultar a IA: {e}")
                st.stop()

            code_match = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
            code = code_match.group(1) if code_match else None
            analise = re.sub(r"```python.*?```", "", content, flags=re.DOTALL).strip()

            resultado = None
            figura = None
            erro_exec = None
            if code:
                try:
                    import numpy as np
                    safe_globals = {
                        "pd": pd, "np": np, "px": px, "go": go,
                        "df_fato": df_fato.copy(), "df_out": df_out.copy(),
                        "df_cat": df_cat.copy(), "df_pvm": df_pvm.copy(),
                        "df_contr": df_contr.copy(),
                    }
                    safe_locals = {}
                    exec(code, safe_globals, safe_locals)
                    resultado = safe_locals.get("resultado")
                    figura = safe_locals.get("figura")
                except Exception as e:
                    erro_exec = f"{type(e).__name__}: {e}"

            st.markdown(analise)
            if erro_exec:
                st.warning(f"⚠️ Erro ao executar o código gerado: {erro_exec}")
                with st.expander("Ver código que falhou"):
                    st.code(code, language="python")
            else:
                if isinstance(resultado, pd.DataFrame):
                    st.dataframe(resultado, use_container_width=True)
                elif resultado is not None:
                    if isinstance(resultado, (int, float)):
                        st.metric("Resultado", f"{resultado:,.2f}")
                    else:
                        st.write(resultado)
                if figura is not None:
                    st.plotly_chart(figura, use_container_width=True)
                with st.expander("Ver código gerado"):
                    st.code(code or "(sem código gerado)", language="python")

            st.session_state.messages.append({
                "role": "assistant",
                "content": analise,
                "code": code,
                "dataframe": resultado if isinstance(resultado, pd.DataFrame) else None,
                "figure": figura,
            })

# ===== Sidebar informativa =====
with st.sidebar:
    st.markdown("### Sobre o chat")
    st.markdown("""
A inteligência artificial gera **código Python** com pandas e Plotly que é executado
localmente sobre os dados consolidados da auditoria.

**Privacidade:** apenas estatísticas descritivas dos dados (min/max/média, listas
de hospitais e OSS) são enviadas à IA — nunca os valores brutos individuais.

**Dica:** para perguntas comparativas, mencione explicitamente quais hospitais
ou OSS você quer comparar.
""")
    if st.button("🧹 Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

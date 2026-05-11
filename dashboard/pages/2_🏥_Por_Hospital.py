"""Drill-down por hospital — timeline financeira, produção, custos, outliers."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    setup_page, load_fato, load_outliers, load_categorias_gasto, load_producao_vs_meta, header,
    COLORS, SCALE_VERDE, SCALE_VERMELHO,
    fmt_brl, fmt_pct,
)

setup_page("Por Hospital", "🏥")
header(
    titulo="Análise por Hospital",
    subtitulo="Drill-down detalhado · indicadores mensais",
)

df = load_fato()
out = load_outliers()
cat = load_categorias_gasto()
pvm = load_producao_vs_meta()

# Hospital selector — aceita pré-seleção via session_state vinda da home
hospitais = sorted(df["hospital"].dropna().unique().tolist())
preset = st.session_state.pop("hospital_filter", None)
if preset and preset in hospitais:
    default_idx = hospitais.index(preset)
elif "HUGOL" in hospitais:
    default_idx = hospitais.index("HUGOL")
else:
    default_idx = 0
hosp = st.selectbox("Selecione o hospital", hospitais, index=default_idx)

dfh = df[df["hospital"] == hosp].sort_values("ano_mes")
oss = dfh["oss"].mode().iloc[0] if not dfh.empty else "-"

# Card com identidade do hospital selecionado
periodo_ini = dfh["ano_mes"].min() if not dfh.empty else "-"
periodo_fim = dfh["ano_mes"].max() if not dfh.empty else "-"
st.markdown(f"""
<div style="margin: 0.5rem 0 1.5rem 0; padding: 1rem 1.25rem; background: {COLORS['verde_pale']};
            border: 1px solid {COLORS['verde_soft']}; border-radius: 12px;
            display: flex; align-items: center; gap: 1.25rem; flex-wrap: wrap;">
    <div style="display: flex; flex-direction: column;">
        <div style="font-family: 'Inter', sans-serif; font-size: 1.5rem; font-weight: 700;
                    color: {COLORS['verde_dark']}; line-height: 1.1; letter-spacing: -0.02em;">{hosp}</div>
        <div style="font-size: 0.8rem; color: {COLORS['text_muted']}; margin-top: 0.2rem;">
            Gestão: <strong style="color: {COLORS['ink']};">{oss}</strong> · Período coberto: {periodo_ini} → {periodo_fim}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# === KPIs ===
c1, c2, c3, c4 = st.columns(4)
c1.metric("Executado (total)", fmt_brl(dfh["executados"].sum()))
c2.metric("% Exec.Financeira", fmt_pct(dfh["perc_exec_financeira"].mean()))
c3.metric("% Exec.Física", fmt_pct(dfh["perc_exec_fisica"].mean()))
c4.metric("Períodos cobertos", str(len(dfh)))

# === Timeline financeira ===
st.markdown("## Movimentação financeira")
fig = go.Figure()
fig.add_trace(go.Bar(
    x=dfh["ano_mes"], y=dfh["recebidos_ses"],
    name="Recebido SES", marker_color=COLORS["verde"],
    hovertemplate="<b>%{x}</b><br>Recebido: R$ %{y:,.0f}<extra></extra>",
))
fig.add_trace(go.Bar(
    x=dfh["ano_mes"], y=dfh["executados"],
    name="Executado", marker_color=COLORS["alerta"],
    hovertemplate="<b>%{x}</b><br>Executado: R$ %{y:,.0f}<extra></extra>",
))
fig.add_trace(go.Bar(
    x=dfh["ano_mes"], y=dfh["devolvidos"],
    name="Devolvido", marker_color=COLORS["dourado"],
    hovertemplate="<b>%{x}</b><br>Devolvido: R$ %{y:,.0f}<extra></extra>",
))
fig.update_layout(
    barmode="group", height=400,
    xaxis_tickangle=-45,
    yaxis=dict(tickformat="~s", tickprefix="R$ ", separatethousands=True),
    margin=dict(l=50, r=20, t=30, b=80),
)
st.plotly_chart(fig, use_container_width=True)

# === Produção + Custos ===
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Atendimentos")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dfh["ano_mes"], y=dfh["consultas"], name="Consultas",
        mode="lines+markers", line=dict(color=COLORS["verde"], width=2),
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=dfh["ano_mes"], y=dfh["internacoes"], name="Internações",
        mode="lines+markers", line=dict(color=COLORS["info"], width=2),
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=dfh["ano_mes"], y=dfh["cirurgias"], name="Cirurgias",
        mode="lines+markers", line=dict(color=COLORS["dourado"], width=2),
        marker=dict(size=5),
    ))
    fig.update_layout(
        height=340, xaxis_tickangle=-45, hovermode="x unified",
        margin=dict(l=50, r=20, t=20, b=70),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Custos unitários (mediana)")
    metrics = {
        "Custo / Consulta": dfh["custo_por_consulta"].median(),
        "Custo / Internação": dfh["custo_por_internacao"].median(),
        "Custo / Leito-Mês": dfh["custo_por_leito_mes"].median(),
        "Custo / Cirurgia": dfh["custo_por_cirurgia"].median(),
    }
    df_m = pd.DataFrame({"métrica": list(metrics.keys()), "valor": list(metrics.values())}).dropna()
    if not df_m.empty:
        fig = go.Figure(go.Bar(
            x=df_m["valor"], y=df_m["métrica"], orientation="h",
            marker=dict(color=df_m["valor"], colorscale=SCALE_VERMELHO, showscale=False),
            text=df_m["valor"].apply(lambda v: f"R$ {v:,.0f}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            height=340, showlegend=False,
            xaxis_tickformat="~s", xaxis_title="", yaxis_title="",
            margin=dict(l=10, r=100, t=20, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados de custos unitários para o período.")

# === Composição de gastos ===
st.markdown("## Composição de gastos por categoria")
cat_h = cat[cat["hospital"] == hosp].copy()
if not cat_h.empty:
    cat_agg = cat_h.groupby("categoria", as_index=False)["valor"].sum().sort_values("valor", ascending=False).head(15).sort_values("valor", ascending=True)
    fig = go.Figure(go.Bar(
        x=cat_agg["valor"], y=cat_agg["categoria"], orientation="h",
        marker=dict(color=cat_agg["valor"], colorscale=SCALE_VERDE, showscale=False),
        text=cat_agg["valor"].apply(lambda v: f"R$ {v:,.0f}"),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        height=520, showlegend=False,
        xaxis_tickformat="~s", xaxis_title="", yaxis_title="",
        margin=dict(l=10, r=110, t=20, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sem dados de categorias de gasto para este hospital.")

# === Outliers do hospital ===
st.markdown("## Atipicidades detectadas")
out_h = out[out["hospital"] == hosp]
if not out_h.empty:
    show = out_h.copy()
    show["valor"] = show["valor"].apply(fmt_brl)
    show["zscore"] = show["zscore"].apply(lambda v: f"{v:.2f}")
    st.dataframe(show[["ano_mes","metric","valor","zscore"]],
                 hide_index=True, use_container_width=True)
else:
    st.success(f"Nenhuma atipicidade significativa em {hosp}.")

# === Tabela detalhada ===
with st.expander("📋 Tabela mensal completa"):
    show = dfh.copy()
    for c in ["recebidos_ses","executados","devolvidos","saldo_final","custo_por_consulta","custo_por_internacao","custo_por_leito_mes","custo_por_cirurgia"]:
        if c in show: show[c] = show[c].apply(fmt_brl)
    for c in ["perc_exec_financeira","perc_exec_fisica","taxa_ocupacao_perc"]:
        if c in show: show[c] = show[c].apply(fmt_pct)
    cols = ["ano_mes","recebidos_ses","executados","devolvidos","saldo_final","perc_exec_financeira","consultas","internacoes","cirurgias","taxa_ocupacao_perc","custo_por_consulta","custo_por_internacao","perc_exec_fisica"]
    cols = [c for c in cols if c in show.columns]
    st.dataframe(show[cols], hide_index=True, use_container_width=True)

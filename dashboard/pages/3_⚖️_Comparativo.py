"""Comparativo entre hospitais ou OSS."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    setup_page, load_fato, header,
    OSS_COLORS, COLORS, SCALE_VERDE, SCALE_VERMELHO,
    fmt_brl, fmt_pct,
)

setup_page("Comparativo", "⚖️")
header(
    titulo="Comparativo entre Unidades",
    subtitulo="Benchmark · Hospital × Hospital · OSS × OSS",
)

df = load_fato()

# === Modo ===
modo = st.radio("Comparar por:", ["Hospital", "OSS"], horizontal=True)
agrup_col = "hospital" if modo == "Hospital" else "oss"

with st.sidebar:
    st.markdown("### Filtros")
    items = sorted(df[agrup_col].dropna().unique().tolist())
    label_modo = "Hospitais para comparar" if modo == "Hospital" else "OSS para comparar"
    sel = st.multiselect(label_modo, items, default=items[:5] if len(items) >= 5 else items,
                         help=f"Selecione até {len(items)} {modo.lower()}s para comparação")
    anos = sorted(df["ano"].dropna().unique().astype(int).tolist())
    anos_recentes = [a for a in anos if a >= 2024]
    with st.expander("Filtro de ano", expanded=False):
        sel_anos = st.multiselect("Ano", anos, default=anos_recentes if anos_recentes else anos,
                                   label_visibility="collapsed")

dff = df[df[agrup_col].isin(sel) & df["ano"].isin(sel_anos)]
if dff.empty:
    st.warning("Sem dados para os filtros selecionados.")
    st.stop()

# === Ranking financeiro ===
st.markdown(f"## Ranking financeiro por {modo.lower()}")
rk = dff.groupby(agrup_col, as_index=False).agg(
    total_recebido=("recebidos_ses", "sum"),
    total_executado=("executados", "sum"),
    total_devolvido=("devolvidos", "sum"),
).sort_values("total_executado", ascending=False)
rk["perc_exec"] = (rk["total_executado"] / rk["total_recebido"] * 100).round(1)
rk_show = rk.copy()
for c in ["total_recebido","total_executado","total_devolvido"]:
    rk_show[c] = rk_show[c].apply(fmt_brl)
rk_show["perc_exec"] = rk_show["perc_exec"].apply(lambda v: fmt_pct(v))
rk_show.columns = [modo, "Total Recebido", "Total Executado", "Total Devolvido", "% Execução"]
st.dataframe(rk_show, hide_index=True, use_container_width=True)

# === Evolução comparada ===
st.markdown("## Evolução mensal — executado (R$)")
df_evo = dff.groupby([agrup_col, "ano_mes"], as_index=False)["executados"].sum().sort_values("ano_mes")
# Color mapping: OSS gets the institutional palette; Hospital gets a derived palette
if modo == "OSS":
    color_map = OSS_COLORS
else:
    # For hospitals, generate a palette from green tones + accents
    items_unique = sorted(df_evo[agrup_col].unique())
    base_palette = [
        COLORS["verde"], COLORS["info"], COLORS["dourado"],
        COLORS["alerta"], COLORS["verde_med"], COLORS["grafite"],
        COLORS["verde_dark"], COLORS["atencao"], COLORS["sucesso"],
        "#5A8C70", "#75407A",
    ]
    color_map = {it: base_palette[i % len(base_palette)] for i, it in enumerate(items_unique)}

fig = go.Figure()
for item in df_evo[agrup_col].unique():
    d = df_evo[df_evo[agrup_col] == item]
    fig.add_trace(go.Scatter(
        x=d["ano_mes"], y=d["executados"],
        name=item, mode="lines+markers",
        line=dict(color=color_map.get(item, COLORS["grafite"]), width=2),
        marker=dict(size=5),
        hovertemplate=f"<b>{item}</b><br>%{{x}}<br>R$ %{{y:,.0f}}<extra></extra>",
    ))
fig.update_layout(
    height=420, xaxis_tickangle=-45, hovermode="x unified",
    yaxis=dict(tickformat="~s", tickprefix="R$ ", separatethousands=True),
    margin=dict(l=50, r=20, t=30, b=80),
)
st.plotly_chart(fig, use_container_width=True)

# === Scatter: % Exec Financ × % Exec Física ===
st.markdown("## Quadrantes: execução financeira × execução física")
st.markdown(
    f"<p style='color: {COLORS['neblina']}; font-size: 0.88rem; margin-top: -0.5em;'>"
    "Tamanho da bolha proporcional ao total executado.</p>",
    unsafe_allow_html=True,
)
df_q = dff.groupby(agrup_col, as_index=False).agg(
    perc_financ=("perc_exec_financeira", "mean"),
    perc_fisica=("perc_exec_fisica", "mean"),
    executado=("executados", "sum"),
)
df_q = df_q.dropna(subset=["perc_financ", "perc_fisica"])
if not df_q.empty:
    df_q["cor"] = df_q[agrup_col].map(color_map).fillna(COLORS["text_muted"])
    # Calcula limites para o "ideal" quadrant (zona verde sutil em torno de 100%×100%)
    fig = go.Figure()
    # Zona ideal sombreada (90-110% em ambos eixos)
    fig.add_shape(
        type="rect", x0=90, x1=110, y0=90, y1=110,
        fillcolor=COLORS["verde_pale"], line=dict(width=0),
        layer="below",
    )
    # Linhas de referência sutis
    fig.add_vline(x=100, line_dash="dot", line_color=COLORS["border"], line_width=1)
    fig.add_hline(y=100, line_dash="dot", line_color=COLORS["border"], line_width=1)
    # Pontos
    fig.add_trace(go.Scatter(
        x=df_q["perc_financ"], y=df_q["perc_fisica"],
        mode="markers+text",
        text=df_q[agrup_col],
        textposition="top center",
        textfont=dict(family="Inter", size=11, color=COLORS["ink"]),
        marker=dict(
            size=df_q["executado"]/df_q["executado"].max()*60 + 10,
            color=df_q["cor"],
            line=dict(color="#FFFFFF", width=2),
            opacity=0.9,
        ),
        customdata=df_q["executado"],
        hovertemplate="<b>%{text}</b><br>Financ.: %{x:.1f}%<br>Física: %{y:.1f}%<br>Executado: R$ %{customdata:,.0f}<extra></extra>",
        showlegend=False,
    ))
    # Apenas 1 label discreto no centro indicando o "alvo"
    fig.add_annotation(
        x=100, y=100, text="alvo",
        showarrow=False,
        font=dict(size=9, color=COLORS["verde"], family="Inter"),
        xshift=20, yshift=20,
    )
    fig.update_layout(
        height=520, showlegend=False,
        xaxis=dict(title="% Execução Financeira", ticksuffix="%"),
        yaxis=dict(title="% Execução Física", ticksuffix="%"),
        margin=dict(l=60, r=30, t=20, b=50),
    )
    st.plotly_chart(fig, use_container_width=True)

# === Comparativo de custo unitário ===
st.markdown("## Custos unitários (mediana)")
metric_options = {
    "Custo / Consulta":     "custo_por_consulta",
    "Custo / Internação":   "custo_por_internacao",
    "Custo / Leito-Mês":    "custo_por_leito_mes",
    "Custo / Cirurgia":     "custo_por_cirurgia",
}
metric_label = st.selectbox("Métrica", list(metric_options.keys()))
metric = metric_options[metric_label]
df_cu = dff.groupby(agrup_col, as_index=False)[metric].median().dropna().sort_values(metric, ascending=True)
fig = go.Figure(go.Bar(
    x=df_cu[metric], y=df_cu[agrup_col], orientation="h",
    marker=dict(color=df_cu[metric], colorscale=SCALE_VERMELHO, showscale=False),
    text=df_cu[metric].apply(lambda v: f"R$ {v:,.0f}"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>",
))
fig.update_layout(
    height=400, showlegend=False,
    xaxis_tickformat="~s", xaxis_title=metric_label, yaxis_title="",
    margin=dict(l=10, r=110, t=20, b=50),
)
st.plotly_chart(fig, use_container_width=True)

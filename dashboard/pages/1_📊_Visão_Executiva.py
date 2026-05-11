"""Visão executiva — KPIs gerais, mapas de calor, evolução."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    setup_page, load_fato, load_outliers, header,
    OSS_COLORS, COLORS, SCALE_VERDE, SCALE_EXEC,
    fmt_brl, fmt_pct,
)

setup_page("Visão Executiva", "📊")

header(
    titulo="Visão Executiva",
    subtitulo="Indicadores agregados · Análise das OSS · SES-GO",
)

df = load_fato()
out = load_outliers()

# === Filtros laterais ===
with st.sidebar:
    st.markdown("### Filtros")
    anos = sorted(df["ano"].dropna().unique().astype(int).tolist())
    anos_recentes = [a for a in anos if a >= 2024]
    with st.expander("Ano", expanded=False):
        sel_anos = st.multiselect("Ano", anos,
                                  default=anos_recentes if anos_recentes else anos,
                                  label_visibility="collapsed")
    oss_list = sorted(df["oss"].dropna().unique().tolist())
    with st.expander("OSS", expanded=False):
        sel_oss = st.multiselect("OSS", oss_list, default=oss_list,
                                 label_visibility="collapsed")
    st.caption(f"Exibindo: {len(sel_anos)} anos · {len(sel_oss)} OSS")

df_f = df[df["ano"].isin(sel_anos) & df["oss"].isin(sel_oss)]

# === KPI cards ===
c1, c2, c3, c4 = st.columns(4)
total_rec = df_f["recebidos_ses"].sum()
total_exe = df_f["executados"].sum()
total_dev = df_f["devolvidos"].sum()
perc_exec = (total_exe / total_rec * 100) if total_rec > 0 else 0
c1.metric("Recebido SES", fmt_brl(total_rec))
c2.metric("Executado", fmt_brl(total_exe))
c3.metric("Devolvido", fmt_brl(total_dev))
c4.metric("% Execução", fmt_pct(perc_exec))

# === Evolução mensal ===
st.markdown("## Evolução mensal")
df_mes = df_f.groupby("ano_mes", as_index=False).agg(
    recebidos=("recebidos_ses", "sum"),
    executados=("executados", "sum"),
    devolvidos=("devolvidos", "sum"),
).sort_values("ano_mes")
df_mes["data"] = pd.to_datetime(df_mes["ano_mes"] + "-01", errors="coerce")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_mes["data"], y=df_mes["recebidos"], mode="lines+markers",
    name="Recebido SES", line=dict(color=COLORS["verde"], width=2.5),
    marker=dict(size=6, color=COLORS["verde"]),
    hovertemplate="<b>%{x|%b/%Y}</b><br>Recebido: R$ %{y:,.0f}<extra></extra>",
))
fig.add_trace(go.Scatter(
    x=df_mes["data"], y=df_mes["executados"], mode="lines+markers",
    name="Executado", line=dict(color=COLORS["alerta"], width=2.5),
    marker=dict(size=6, color=COLORS["alerta"]),
    hovertemplate="<b>%{x|%b/%Y}</b><br>Executado: R$ %{y:,.0f}<extra></extra>",
))
fig.add_trace(go.Scatter(
    x=df_mes["data"], y=df_mes["devolvidos"], mode="lines+markers",
    name="Devolvido", line=dict(color=COLORS["dourado"], width=1.8, dash="dot"),
    marker=dict(size=5, color=COLORS["dourado"]),
    hovertemplate="<b>%{x|%b/%Y}</b><br>Devolvido: R$ %{y:,.0f}<extra></extra>",
))
fig.update_layout(
    height=380, hovermode="x unified",
    yaxis_title="", xaxis_title="",
    margin=dict(l=50, r=20, t=30, b=40),
)
fig.update_yaxes(tickformat="~s", tickprefix="R$ ", separatethousands=True)
st.plotly_chart(fig, use_container_width=True)

# === Por OSS e Hospital ===
col_oss, col_hosp = st.columns(2)

with col_oss:
    st.markdown("### Total executado por OSS")
    df_oss = df_f.groupby("oss", as_index=False)["executados"].sum().sort_values("executados", ascending=True)
    max_val = df_oss["executados"].max() if not df_oss.empty else 0
    fig = go.Figure(go.Bar(
        x=df_oss["executados"], y=df_oss["oss"], orientation="h",
        marker=dict(color=[OSS_COLORS.get(o, COLORS["grafite"]) for o in df_oss["oss"]]),
        text=df_oss["executados"].apply(lambda v: f" R$ {v/1e6:,.1f} mi".replace(",", ".")),
        textposition="outside",
        textfont=dict(family="Inter", size=12, color=COLORS["ink"]),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Executado: R$ %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        height=max(360, 32 * len(df_oss) + 80), showlegend=False,
        xaxis_title="", yaxis_title="",
        margin=dict(l=10, r=140, t=20, b=40),
    )
    fig.update_xaxes(tickformat="~s", tickprefix="R$ ", separatethousands=True,
                     range=[0, max_val * 1.18] if max_val else None)
    st.plotly_chart(fig, use_container_width=True)

with col_hosp:
    st.markdown("### Top 10 hospitais (executado)")
    df_hosp = df_f.groupby("hospital", as_index=False)["executados"].sum().sort_values("executados", ascending=False).head(10).sort_values("executados", ascending=True)
    max_val = df_hosp["executados"].max() if not df_hosp.empty else 0
    fig = go.Figure(go.Bar(
        x=df_hosp["executados"], y=df_hosp["hospital"], orientation="h",
        marker=dict(color=df_hosp["executados"], colorscale=SCALE_VERDE, showscale=False),
        text=df_hosp["executados"].apply(lambda v: f" R$ {v/1e6:,.1f} mi".replace(",", ".")),
        textposition="outside",
        textfont=dict(family="Inter", size=12, color=COLORS["ink"]),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Executado: R$ %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        height=max(360, 32 * len(df_hosp) + 80), showlegend=False,
        xaxis_title="", yaxis_title="",
        margin=dict(l=10, r=140, t=20, b=40),
    )
    fig.update_xaxes(tickformat="~s", tickprefix="R$ ", separatethousands=True,
                     range=[0, max_val * 1.18] if max_val else None)
    st.plotly_chart(fig, use_container_width=True)

# === Mapa de calor ===
st.markdown("## Mapa de calor: % execução financeira")
st.markdown(
    f"<p style='color: {COLORS['neblina']}; font-size: 0.88rem; margin-top: -0.5em;'>"
    "Cores em escala institucional — vermelho indica baixa execução, verde escuro indica alta execução.</p>",
    unsafe_allow_html=True,
)
df_h = df_f.dropna(subset=["perc_exec_financeira"])
if not df_h.empty:
    pivot = df_h.pivot_table(index="hospital", columns="ano_mes", values="perc_exec_financeira", aggfunc="mean")
    # Reordenar Y por mediana de execução (mais consistente em cima)
    pivot = pivot.loc[pivot.median(axis=1).sort_values(ascending=False).index]
    pivot_clip = pivot.clip(upper=150)
    # Escala limpa: cinza claro (sub-execução) → verde (alvo)
    custom_scale = [
        (0.0,  "#F3F4F6"),
        (0.4,  "#FCD34D"),
        (0.67, "#22A55F"),  # 100% = alvo
        (1.0,  "#063D1F"),
    ]
    fig = go.Figure(go.Heatmap(
        z=pivot_clip.values,
        x=list(pivot_clip.columns),
        y=list(pivot_clip.index),
        colorscale=custom_scale,
        zmin=0, zmax=150,
        colorbar=dict(
            title=dict(text="% Exec.", font=dict(family="Inter", size=10, color=COLORS["text_muted"])),
            tickfont=dict(family="Inter", size=10, color=COLORS["text_muted"]),
            outlinewidth=0,
            len=0.85, thickness=8,
            tickvals=[0, 50, 100, 150],
            ticktext=["0%", "50%", "100%", "≥150%"],
        ),
        xgap=2, ygap=2,
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        height=max(360, 32 * len(pivot_clip.index) + 100),
        xaxis=dict(tickangle=-45, side="bottom"),
        yaxis=dict(side="left", autorange="reversed"),
        margin=dict(l=100, r=20, t=20, b=80),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

# === Outliers ===
st.markdown("## Atipicidades de custo unitário")
st.markdown(
    f"<p style='color: {COLORS['neblina']}; font-size: 0.88rem; margin-top: -0.5em;'>"
    "Períodos com z-score ≥ 2,5 em relação à coorte. Pode indicar ramp-up, especialização ou anomalia operacional.</p>",
    unsafe_allow_html=True,
)
if not out.empty:
    out_show = out.copy()
    out_show["valor"] = out_show["valor"].apply(fmt_brl)
    out_show["zscore"] = out_show["zscore"].apply(lambda v: f"{v:.2f}")
    out_show = out_show[["hospital", "oss", "ano_mes", "metric", "valor", "zscore"]]
    out_show.columns = ["Hospital", "OSS", "Período", "Métrica", "Valor", "z-score"]
    st.dataframe(out_show, hide_index=True, use_container_width=True)

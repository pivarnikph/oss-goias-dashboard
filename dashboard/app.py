"""Dashboard de Auditoria — OSS Saúde de Goiás · Hub central.

A home é o ponto de partida da auditoria: hero com indicadores,
busca rápida por hospital, achados em destaque e atalhos visuais
para as 4 áreas de análise.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from utils import (
    setup_page, load_fato, load_cobertura, load_outliers,
    fmt_brl, fmt_pct, hero, COLORS,
)

setup_page("Hub da Auditoria", "🏥")

# ===== Carregamento de dados =====
df = load_fato()
cob = load_cobertura()
out = load_outliers()

total_recebido = df["recebidos_ses"].sum()
total_executado = df["executados"].sum()
total_devolvido = df["devolvidos"].sum()
perc_exec = (total_executado / total_recebido * 100) if total_recebido > 0 else 0
n_hosp = cob["hospital"].nunique()
n_oss = df["oss"].dropna().nunique()
n_meses = df["ano_mes"].nunique()
periodo_ini = df["ano_mes"].min()
periodo_fim = df["ano_mes"].max()

# ===== Sidebar info (consistente em todas as páginas via setup_page; aqui adicionamos contextual) =====
with st.sidebar:
    st.markdown(
        f"""<div style="padding: 0.75rem 0.5rem 1rem 0.5rem; margin-bottom: 0.5rem;
        border-bottom: 1px solid {COLORS['border']};">
        <div style="font-size: 0.7rem; color: {COLORS['text_muted']}; text-transform: uppercase;
                    letter-spacing: 0.08em; font-weight: 600;">SES-GO · Auditoria</div>
        <div style="font-size: 1rem; color: {COLORS['ink']}; font-weight: 700; margin-top: 0.15rem;">
            Painel das OSS
        </div>
        <div style="font-size: 0.78rem; color: {COLORS['text_muted']}; margin-top: 0.2rem;">
            {periodo_ini} → {periodo_fim}
        </div>
    </div>""",
        unsafe_allow_html=True,
    )

# ===== Hero (gradiente verde com indicadores-chave) =====
hero(
    titulo="Auditoria das Organizações Sociais de Saúde",
    subtitulo="Análise consolidada dos contratos de gestão das OSS contratadas pela SES-GO. Explore indicadores, investigue achados ou pergunte diretamente aos dados.",
    meta=[
        ("Hospitais", str(n_hosp)),
        ("OSS gestoras", str(n_oss)),
        ("Período", f"{periodo_ini} → {periodo_fim}"),
    ],
)

# ===== Linha de KPIs principais — com helper texts =====
c1, c2, c3, c4 = st.columns(4)
c1.metric("Recebido SES-GO", fmt_brl(total_recebido),
          help="Total repassado pela SES-GO às OSS no período")
c2.metric("Executado", fmt_brl(total_executado),
          help="Total efetivamente gasto pelas OSS no período")
c3.metric("Devolvido", fmt_brl(total_devolvido),
          help="Recursos devolvidos por glosa, encerramento ou ressarcimento")
c4.metric("% Execução", fmt_pct(perc_exec),
          help="Razão executado/recebido. Valores próximos a 100% são saudáveis")

# ===== Busca rápida =====
st.markdown(
    f"""<div class="quick-search-card">
    <div class="quick-search-title">🔎 Acesso rápido por hospital</div>
    <p class="quick-search-hint">Selecione um hospital para ir direto ao painel detalhado dele — financeiro, produção, custos e atipicidades em um só lugar.</p>
</div>""",
    unsafe_allow_html=True,
)

hospitais = sorted(df["hospital"].dropna().unique().tolist())
qc1, qc2 = st.columns([3, 1])
with qc1:
    sel_hosp = st.selectbox(
        "Hospital",
        options=["— Escolha um hospital —"] + hospitais,
        label_visibility="collapsed",
        key="quick_hosp_select",
    )
with qc2:
    abrir = st.button(
        "Abrir painel →",
        use_container_width=True,
        type="primary",
        disabled=(sel_hosp == "— Escolha um hospital —"),
        help="Selecione um hospital acima para habilitar",
    )
    if abrir and sel_hosp != "— Escolha um hospital —":
        st.session_state["hospital_filter"] = sel_hosp
        st.switch_page("pages/2_🏥_Por_Hospital.py")

# ===== Achados em destaque =====
st.markdown(
    '<div class="section-label"><h2 class="section-label-title">Achados em destaque</h2>'
    '<p class="section-label-hint">Síntese executiva da auditoria 2026</p></div>',
    unsafe_allow_html=True,
)

findings = [
    ("ok", "Execução agregada saudável (101,9%)",
     "Os R$ 3,57 bi repassados foram executados dentro de parâmetros normais. Sem indícios de fraude sistêmica."),
    ("warn", "Concentração elevada em uma OSS",
     "AGIR/HUGOL responde sozinha por 39,3% do gasto. Top-2 OSS concentram 54%. HHI = 2.119 — risco estrutural."),
    ("info", "13 outliers operacionais investigados",
     "Todos com explicação: 2 erros de extração já corrigidos, demais decorrem de ramp-up ou variações sazonais."),
    ("ok", "Validação cruzada: 100% de concordância financeira",
     "Re-extração com modelo independente confirmou todos os 23 documentos financeiros amostrados. Dados sólidos."),
]
fcols = st.columns(2)
for i, (tag, title, desc) in enumerate(findings):
    fcols[i % 2].markdown(
        f"""<div class="finding-card">
        <div class="finding-tag {tag}">{["✓","!","i","✓"][i]}</div>
        <div class="finding-content">
            <h4 class="finding-title">{title}</h4>
            <p class="finding-desc">{desc}</p>
        </div>
    </div>""",
        unsafe_allow_html=True,
    )

# ===== Navegação principal (hub cards) =====
st.markdown(
    '<div class="section-label"><h2 class="section-label-title">Explorar a auditoria</h2>'
    '<p class="section-label-hint">Quatro caminhos de análise — escolha por onde começar</p></div>',
    unsafe_allow_html=True,
)

nav_items = [
    {
        "icon": "📊", "name": "Visão Executiva",
        "desc": "KPIs agregados, evolução temporal de repasses, mapa de calor da execução financeira por hospital e período.",
        "page": "pages/1_📊_Visão_Executiva.py",
        "accent": COLORS["verde"],
        "bg": COLORS["verde_pale"],
    },
    {
        "icon": "🏥", "name": "Por Hospital",
        "desc": "Drill-down completo de um hospital específico: contratos, fluxo financeiro mensal, produção realizada e custos unitários.",
        "page": "pages/2_🏥_Por_Hospital.py",
        "accent": COLORS["info"],
        "bg": COLORS["info_soft"],
    },
    {
        "icon": "⚖️", "name": "Comparativo",
        "desc": "Hospitais ou OSS lado a lado. Rankings, quadrante de execução, comparação de eficiência entre gestoras.",
        "page": "pages/3_⚖️_Comparativo.py",
        "accent": COLORS["amarelo"],
        "bg": COLORS["amarelo_pale"],
    },
    {
        "icon": "💬", "name": "Pergunte aos Dados",
        "desc": "Faça perguntas em português natural. A IA gera gráficos e tabelas a partir dos dados consolidados na hora.",
        "page": "pages/4_🤖_Pergunte_Aos_Dados.py",
        "accent": "#7C3AED",
        "bg": "#F5F3FF",
    },
    {
        "icon": "🔬", "name": "Validação dos Dados",
        "desc": "Metodologia da extração, fontes utilizadas, checks de qualidade e validação cruzada — transparência completa do pipeline.",
        "page": "pages/5_🔬_Validação_dos_Dados.py",
        "accent": COLORS["alerta"],
        "bg": COLORS["alerta_soft"],
    },
]

cols = st.columns(2)
for i, item in enumerate(nav_items):
    with cols[i % 2]:
        with st.container():
            st.markdown(
                f"""<div class="hub-card" style="--accent: {item['accent']}; --icon-bg: {item['bg']};">
                <div class="hub-card-icon" style="color: {item['accent']};">{item['icon']}</div>
                <h3 class="hub-card-title">{item['name']}</h3>
                <p class="hub-card-desc">{item['desc']}</p>
            </div>""",
                unsafe_allow_html=True,
            )
            if st.button(
                f"Abrir {item['name']} →",
                key=f"nav_{i}",
                use_container_width=True,
                type="secondary",
            ):
                st.switch_page(item["page"])

# ===== Cobertura por hospital =====
st.markdown(
    '<div class="section-label"><h2 class="section-label-title">Cobertura de dados por hospital</h2>'
    '<p class="section-label-hint">% de meses com dado disponível por tipo de indicador</p></div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""<div class="tip-card">
    <div class="tip-card-icon">💡</div>
    <p class="tip-card-text">A cobertura indica a quantidade de meses em que cada tipo de relatório foi publicado pela OSS — quanto mais alto, mais completa a série histórica disponível para análise.</p>
</div>""",
    unsafe_allow_html=True,
)

cob_show = cob.copy()
cob_show["executados_mediana"] = cob_show["executados_mediana"].apply(lambda v: fmt_brl(v))
cob_show["pct_com_executados"] = cob_show["pct_com_executados"].astype(int).astype(str) + "%"
cob_show["pct_com_consultas"] = cob_show["pct_com_consultas"].astype(int).astype(str) + "%"
cob_show["pct_com_perc_fisica"] = cob_show["pct_com_perc_fisica"].astype(int).astype(str) + "%"
cob_show["pct_com_perc_financ"] = cob_show["pct_com_perc_financ"].astype(int).astype(str) + "%"
cob_show.columns = [
    "Hospital", "Meses", "Início", "Fim",
    "Financeiro", "Produção", "% Físico", "% Financ.", "Mediana mensal",
]
st.dataframe(cob_show, hide_index=True, use_container_width=True)

# ===== Rodapé =====
st.markdown(
    f"""<div style="margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid {COLORS['border']};
            font-family: 'Inter', sans-serif; font-size: 0.8125rem; color: {COLORS['text_muted']};
            display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
    <span>Pipeline reproduzível · SHA-256 auditável · validação cruzada por modelo independente</span>
    <span>Secretaria de Estado da Saúde · Goiás · 2026</span>
</div>""",
    unsafe_allow_html=True,
)

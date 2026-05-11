"""Tema do dashboard — hub central da análise OSS-GO.

Princípios:
- Hub central: home convida exploração, atalhos visíveis, achados em destaque
- Contraste forte: textos secundários #4B5563+ em fundo branco (WCAG AA)
- Tipografia única Inter para coerência
- Verde Goiás como accent intencional; cinza neutro como base
- Componentes ricos: badges, hero, stat-tiles, finding-cards
"""
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# === PALETA ===
COLORS = {
    # Background / surface
    "bg":           "#FFFFFF",
    "surface":      "#FFFFFF",
    "subtle":       "#F9FAFB",   # gray-50
    "muted":        "#F3F4F6",   # gray-100
    "muted_strong": "#E5E7EB",   # gray-200

    # Borders
    "border":        "#E5E7EB",
    "border_strong": "#D1D5DB",

    # Text — contraste reforçado
    "ink":          "#0F172A",   # primário (slate-900) — AAA em #FFF
    "text":         "#1F2937",   # secundário (gray-800) — AA forte
    "text_muted":   "#4B5563",   # terciário (gray-600) — AA — limite mínimo
    "text_subtle":  "#6B7280",   # apenas para microcopy não-crítico

    # Accent — Goiás verde
    "verde":        "#0D703E",
    "verde_dark":   "#063D1F",
    "verde_med":    "#22A55F",
    "verde_soft":   "#E8F1EC",
    "verde_pale":   "#F4F8F5",

    # Accent — dourado sóbrio
    "amarelo":      "#B8860B",   # mais escuro, melhor contraste
    "amarelo_pale": "#FEF3C7",

    # Estados — todos com contraste AA
    "sucesso":      "#15803D",
    "sucesso_soft": "#DCFCE7",
    "alerta":       "#B91C1C",
    "alerta_soft":  "#FEE2E2",
    "atencao":      "#92400E",
    "atencao_soft": "#FED7AA",
    "info":         "#1D4ED8",
    "info_soft":    "#DBEAFE",

    # legacy aliases (não remover — vários arquivos usam)
    "tinta":        "#0F172A",
    "grafite":      "#1F2937",
    "neblina":      "#4B5563",
    "linha":        "#E5E7EB",
    "papel":        "#FFFFFF",
    "card":         "#FFFFFF",
    "borda":        "#E5E7EB",
    "verde_light":  "#E8F1EC",
    "dourado":      "#B8860B",
}

FONTS = {
    "sans": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "mono": "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace",
    "display": "'Inter', -apple-system, sans-serif",
    "body":    "'Inter', -apple-system, sans-serif",
}

OSS_COLORS = {
    "AGIR":             "#0D703E",
    "FUNEV":            "#22A55F",
    "ISG":              "#1D4ED8",
    "IMED":             "#7C3AED",
    "IGH":              "#0891B2",
    "IPGSE":            "#C2410C",
    "Hospital de Amor": "#BE185D",
    "Albert Einstein":  "#0F766E",
    "ABEVIDA":          "#92400E",
    "Instituto Patris": "#4B5563",
    "IDTech":           "#B8860B",
}

SCALE_VERDE = [(0.0, "#F4F8F5"), (0.5, "#22A55F"), (1.0, "#063D1F")]
SCALE_VERMELHO = [(0.0, "#FEF2F2"), (0.5, "#EF4444"), (1.0, "#7F1D1D")]
SCALE_EXEC = [
    (0.0,   "#F3F4F6"),
    (0.25,  "#FECACA"),
    (0.45,  "#FCD34D"),
    (0.5,   "#22A55F"),
    (0.75,  "#0D703E"),
    (1.0,   "#063D1F"),
]
SCALE_DOURADO = [(0.0, "#FEF3C7"), (0.5, "#B8860B"), (1.0, "#78350F")]


def _build_css():
    c = COLORS
    f = FONTS
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ========== BASE ========== */
html, body, [data-testid="stApp"], [class*="css"] {{
    font-family: {f['sans']};
    color: {c['ink']};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-feature-settings: "cv02", "cv03", "cv04", "cv11", "tnum";
}}

[data-testid="stApp"] {{
    background: {c['bg']};
}}

.main .block-container {{
    padding-top: 2.5rem;
    padding-bottom: 5rem;
    max-width: 1280px;
}}

/* ========== HEADINGS ========== */
h1, h2, h3, h4 {{
    font-family: {f['sans']};
    color: {c['ink']};
    letter-spacing: -0.02em;
    font-weight: 600;
}}

h1 {{ font-size: 2rem; line-height: 1.15; margin: 0 0 0.5em 0; font-weight: 700; letter-spacing: -0.03em; }}
h2 {{ font-size: 1.25rem; margin: 2.5em 0 1em 0; font-weight: 600; color: {c['ink']}; }}
h3 {{ font-size: 1rem; margin: 1.75em 0 0.75em 0; color: {c['ink']}; font-weight: 600; }}

p, li, label, span:not([class]) {{
    font-family: {f['sans']};
    color: {c['text']};
    line-height: 1.6;
    font-size: 0.95rem;
}}

code {{
    font-family: {f['mono']};
    font-size: 0.85em;
    background: {c['muted']};
    color: {c['ink']};
    padding: 0.1em 0.35em;
    border-radius: 4px;
}}

a {{ color: {c['verde']}; text-decoration: none; font-weight: 500; }}
a:hover {{ text-decoration: underline; }}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {{
    background: {c['subtle']};
    border-right: 1px solid {c['border']};
}}

[data-testid="stSidebar"] *:not(input):not(textarea):not(select) {{
    color: {c['text']};
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {c['ink']};
}}

[data-testid="stSidebarNav"] li a {{
    color: {c['text']} !important;
    font-family: {f['sans']};
    font-weight: 500;
    font-size: 0.9rem;
    border-radius: 8px;
    padding: 0.55rem 0.8rem !important;
    transition: all 0.15s;
}}

/* Renomeia a primeira entrada da nav (que seria "app") para "Início" via CSS */
[data-testid="stSidebarNav"] ul li:first-child a {{
    position: relative;
}}

[data-testid="stSidebarNav"] ul li:first-child a > span {{
    visibility: hidden;
}}

[data-testid="stSidebarNav"] ul li:first-child a::before {{
    content: "🏠  Início";
    position: absolute;
    left: 0.8rem;
    top: 50%;
    transform: translateY(-50%);
    color: {c['ink']};
    font-weight: 600;
    font-size: 0.9rem;
    font-family: {f['sans']};
    pointer-events: none;
    white-space: nowrap;
}}

[data-testid="stSidebarNav"] ul li:first-child a[aria-current="page"]::before {{
    color: {c['verde_dark']};
}}

[data-testid="stSidebarNav"] li a:hover {{
    color: {c['ink']} !important;
    background: {c['muted']};
}}

[data-testid="stSidebarNav"] li a[aria-current="page"] {{
    color: {c['verde_dark']} !important;
    background: {c['verde_soft']};
    font-weight: 600;
}}

/* ========== MÉTRICAS ========== */
[data-testid="stMetric"] {{
    background: {c['surface']};
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    border: 1px solid {c['border']};
    box-shadow: none;
    transition: all 0.18s ease;
}}

[data-testid="stMetric"]:hover {{
    border-color: {c['border_strong']};
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.05);
    transform: translateY(-1px);
}}

[data-testid="stMetricLabel"] p {{
    font-family: {f['sans']} !important;
    font-size: 0.8125rem !important;
    color: {c['text_muted']} !important;
    font-weight: 500;
    margin: 0 0 0.35rem 0 !important;
    letter-spacing: 0;
    text-transform: none;
}}

[data-testid="stMetricValue"] {{
    font-family: {f['sans']} !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: {c['ink']} !important;
    letter-spacing: -0.025em !important;
    line-height: 1.2 !important;
    font-feature-settings: "tnum" on;
}}

[data-testid="stMetricDelta"] {{
    font-family: {f['sans']} !important;
    font-size: 0.8125rem !important;
    font-weight: 500;
}}

/* ========== BOTÕES ========== */
.stButton > button {{
    background: {c['ink']};
    color: #FFFFFF;
    border: 1px solid {c['ink']};
    font-family: {f['sans']};
    font-weight: 500;
    font-size: 0.875rem;
    padding: 0.55rem 1.1rem;
    border-radius: 8px;
    transition: all 0.15s;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}}

.stButton > button:hover {{
    background: {c['text']};
    border-color: {c['text']};
    color: #FFFFFF;
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}}

.stButton > button:active {{
    transform: translateY(0);
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}}

/* Botão secundário na sidebar */
[data-testid="stSidebar"] .stButton > button {{
    background: #FFFFFF;
    color: {c['ink']} !important;
    border: 1px solid {c['border']};
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: {c['muted']};
    color: {c['ink']} !important;
    border-color: {c['border_strong']};
}}

/* Botões 'sample question' — estilo pill suave */
.stButton > button[kind="secondary"] {{
    background: {c['verde_pale']};
    color: {c['verde_dark']} !important;
    border: 1px solid {c['verde_soft']};
    font-weight: 500;
    text-align: left;
    justify-content: flex-start;
}}

.stButton > button[kind="secondary"]:hover {{
    background: {c['verde_soft']};
    color: {c['verde_dark']} !important;
    border-color: {c['verde_med']};
}}

/* ========== INPUTS ========== */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="select"] > div,
[data-baseweb="input"] > div {{
    border-radius: 8px !important;
    border: 1px solid {c['border']} !important;
    font-family: {f['sans']};
    background: {c['surface']} !important;
    color: {c['ink']} !important;
}}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: {c['verde']} !important;
    box-shadow: 0 0 0 3px {c['verde_soft']} !important;
    outline: none !important;
}}

/* Segmented control (radios inline) */
[data-testid="stRadio"] [role="radiogroup"] {{
    background: {c['muted']};
    padding: 0.25rem;
    border-radius: 10px;
    display: inline-flex;
    gap: 0;
}}

[data-testid="stRadio"] [role="radiogroup"] label {{
    margin: 0;
    padding: 0.45rem 1.1rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    color: {c['text']};
    transition: all 0.15s;
}}

[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {{
    background: {c['surface']};
    color: {c['ink']};
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}

/* ========== EXPANDERS ========== */
[data-testid="stExpander"] {{
    border: 1px solid {c['border']};
    border-radius: 12px;
    background: {c['surface']};
    box-shadow: none;
}}

[data-testid="stExpander"] summary {{
    font-family: {f['sans']};
    font-weight: 500;
    font-size: 0.9rem;
    color: {c['text']};
    padding: 0.85rem 1.1rem;
}}

[data-testid="stExpander"] summary:hover {{ color: {c['ink']}; }}

/* ========== DATAFRAMES ========== */
[data-testid="stDataFrame"] {{
    border: 1px solid {c['border']};
    border-radius: 12px;
    overflow: hidden;
    background: {c['surface']};
}}

[data-testid="stDataFrame"] thead th {{
    background: {c['subtle']} !important;
    color: {c['ink']} !important;
    font-family: {f['sans']};
    font-weight: 600 !important;
    font-size: 0.8125rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    border-bottom: 1px solid {c['border']} !important;
    padding: 0.75rem 0.85rem !important;
}}

[data-testid="stDataFrame"] tbody td {{
    font-family: {f['sans']};
    font-feature-settings: "tnum" on;
    font-size: 0.875rem;
    color: {c['ink']};
    padding: 0.65rem 0.85rem !important;
}}

[data-testid="stDataFrame"] tbody tr:hover td {{ background: {c['subtle']} !important; }}

/* ========== CHAT ========== */
[data-testid="stChatMessage"] {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 14px;
    padding: 1.1rem 1.35rem;
    margin-bottom: 0.85rem;
    box-shadow: none;
}}

[data-testid="stChatMessage"][class*="user"] {{
    background: {c['verde_pale']};
    border-color: {c['verde_soft']};
}}

[data-testid="stChatInput"] textarea {{
    border-radius: 12px !important;
    border-color: {c['border']} !important;
    font-family: {f['sans']};
    color: {c['ink']} !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: {c['text_muted']} !important;
}}

/* ========== DIVIDERS ========== */
hr {{
    border: 0;
    border-top: 1px solid {c['border']};
    margin: 3rem 0 1.5rem 0;
}}

/* ========== ALERTAS ========== */
.stAlert {{ border-radius: 12px; border-width: 1px; }}

/* ========== HERO HEADER (página inicial) ========== */
.hub-hero {{
    background: linear-gradient(135deg, {c['verde_dark']} 0%, {c['verde']} 100%);
    color: #FFFFFF;
    padding: 2.5rem 2.5rem 2.25rem 2.5rem;
    border-radius: 16px;
    margin: 0 0 2rem 0;
    position: relative;
    overflow: hidden;
}}

.hub-hero::before {{
    content: "";
    position: absolute;
    top: -30%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}}

.hub-hero-eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8125rem;
    font-weight: 600;
    color: rgba(255,255,255,0.85);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin: 0 0 0.85rem 0;
}}

.hub-hero-eyebrow::before {{
    content: "";
    width: 7px; height: 7px;
    background: #FCD34D;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 0 4px rgba(252,211,77,0.25);
}}

.hub-hero-title {{
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    line-height: 1.1;
    margin: 0 0 0.6rem 0 !important;
    letter-spacing: -0.03em;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 8px rgba(0,0,0,0.25);
}}

.hub-hero h1.hub-hero-title,
.hub-hero h1 {{
    color: #FFFFFF !important;
    font-weight: 800 !important;
}}

.hub-hero-subtitle {{
    font-size: 1.0625rem;
    color: rgba(255,255,255,0.92);
    margin: 0;
    font-weight: 400;
    line-height: 1.5;
    max-width: 720px;
    position: relative;
    z-index: 1;
}}

.hub-hero-meta {{
    display: flex;
    gap: 1.5rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}}

.hub-hero-meta-item {{
    display: flex;
    flex-direction: column;
    color: rgba(255,255,255,0.95);
}}

.hub-hero-meta-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: rgba(255,255,255,0.7);
    margin-bottom: 0.15rem;
}}

.hub-hero-meta-value {{
    font-size: 1.25rem;
    font-weight: 600;
    color: #FFFFFF;
    font-feature-settings: "tnum" on;
}}

/* ========== HEADER PADRÃO INTERNO (páginas não-home) ========== */
.clean-header {{
    margin: 0 0 2.5rem 0;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid {c['border']};
}}

.clean-eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: {f['sans']};
    font-size: 0.8125rem;
    font-weight: 600;
    color: {c['verde']};
    letter-spacing: 0;
    margin: 0 0 0.6rem 0;
    text-transform: none;
}}

.clean-eyebrow::before {{
    content: "";
    width: 6px; height: 6px;
    background: {c['verde']};
    border-radius: 50%;
    display: inline-block;
}}

.clean-title {{
    font-family: {f['sans']};
    font-size: 1.875rem !important;
    font-weight: 700;
    color: {c['ink']};
    line-height: 1.15;
    margin: 0 0 0.4rem 0 !important;
    letter-spacing: -0.03em;
}}

.clean-subtitle {{
    font-family: {f['sans']};
    font-size: 1rem;
    color: {c['text_muted']};
    margin: 0;
    font-weight: 400;
    line-height: 1.5;
}}

.clean-pill {{
    display: inline-flex;
    align-items: center;
    background: {c['verde_pale']};
    color: {c['verde_dark']};
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-family: {f['sans']};
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0;
    margin-left: 0.7rem;
    vertical-align: middle;
    border: 1px solid {c['verde_soft']};
}}

/* ========== CARD NAVEGAÇÃO (home — hub) ========== */
.hub-card {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 14px;
    padding: 1.5rem 1.5rem 1.35rem 1.5rem;
    transition: all 0.2s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}}

.hub-card::before {{
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--accent, {c['verde']});
    opacity: 0;
    transition: opacity 0.2s;
}}

.hub-card:hover {{
    border-color: {c['border_strong']};
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
}}

.hub-card:hover::before {{ opacity: 1; }}

.hub-card-icon {{
    width: 44px; height: 44px;
    border-radius: 10px;
    background: var(--icon-bg, {c['verde_pale']});
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 0.25rem;
}}

.hub-card-title {{
    font-size: 1.0625rem;
    font-weight: 600;
    color: {c['ink']};
    margin: 0;
    line-height: 1.3;
}}

.hub-card-desc {{
    font-size: 0.9rem;
    color: {c['text_muted']};
    line-height: 1.55;
    margin: 0;
    flex: 1;
}}

.hub-card-arrow {{
    font-size: 0.875rem;
    color: {c['verde']};
    font-weight: 600;
    margin-top: 0.25rem;
}}

/* ========== STAT TILE (home) ========== */
.stat-tile {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    height: 100%;
}}

.stat-tile-label {{
    font-size: 0.75rem;
    font-weight: 500;
    color: {c['text_muted']};
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0 0 0.45rem 0;
}}

.stat-tile-value {{
    font-size: 1.625rem;
    font-weight: 700;
    color: {c['ink']};
    line-height: 1.1;
    margin: 0 0 0.2rem 0;
    font-feature-settings: "tnum" on;
    letter-spacing: -0.025em;
}}

.stat-tile-hint {{
    font-size: 0.8125rem;
    color: {c['text_muted']};
    margin: 0;
    line-height: 1.4;
}}

/* ========== FINDING CARDS (achados em destaque) ========== */
.finding-card {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    display: flex;
    gap: 0.95rem;
    align-items: flex-start;
    transition: all 0.15s;
    height: 100%;
}}

.finding-card:hover {{
    border-color: {c['border_strong']};
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}

.finding-tag {{
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px; height: 26px;
    border-radius: 7px;
    font-size: 0.75rem;
    font-weight: 700;
    color: #FFFFFF;
}}

.finding-tag.ok    {{ background: {c['sucesso']}; }}
.finding-tag.warn  {{ background: {c['atencao']}; }}
.finding-tag.crit  {{ background: {c['alerta']}; }}
.finding-tag.info  {{ background: {c['info']}; }}

.finding-content {{ flex: 1; min-width: 0; }}

.finding-title {{
    font-size: 0.95rem;
    font-weight: 600;
    color: {c['ink']};
    margin: 0 0 0.25rem 0;
    line-height: 1.35;
}}

.finding-desc {{
    font-size: 0.875rem;
    color: {c['text']};
    margin: 0;
    line-height: 1.5;
}}

/* ========== BADGES ========== */
.badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    border: 1px solid transparent;
}}

.badge-ok    {{ background: {c['sucesso_soft']}; color: {c['sucesso']}; border-color: #BBF7D0; }}
.badge-warn  {{ background: {c['atencao_soft']}; color: {c['atencao']}; border-color: #FED7AA; }}
.badge-crit  {{ background: {c['alerta_soft']}; color: {c['alerta']}; border-color: #FECACA; }}
.badge-info  {{ background: {c['info_soft']}; color: {c['info']}; border-color: #BFDBFE; }}
.badge-neutral {{ background: {c['muted']}; color: {c['text']}; border-color: {c['border']}; }}

/* Section helper */
.section-label {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin: 2.5rem 0 1rem 0;
}}

.section-label-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: {c['ink']};
    margin: 0;
    letter-spacing: -0.015em;
}}

.section-label-hint {{
    font-size: 0.85rem;
    color: {c['text_muted']};
    margin: 0;
}}

/* Quick search card (hub) */
.quick-search-card {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin: 0 0 1.5rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}}

.quick-search-title {{
    font-size: 1.0625rem;
    font-weight: 600;
    color: {c['ink']};
    margin: 0 0 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.quick-search-hint {{
    font-size: 0.875rem;
    color: {c['text_muted']};
    margin: 0;
}}

/* Tips card (gentil) */
.tip-card {{
    background: {c['verde_pale']};
    border: 1px solid {c['verde_soft']};
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    display: flex;
    gap: 0.7rem;
    align-items: flex-start;
    margin: 0 0 1rem 0;
}}

.tip-card-icon {{ font-size: 1.05rem; flex-shrink: 0; }}
.tip-card-text {{ font-size: 0.875rem; color: {c['verde_dark']}; line-height: 1.5; margin: 0; }}

/* Esconder chrome do Streamlit */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header[data-testid="stHeader"] {{
    background: transparent;
    height: 0;
}}

/* tnum global */
* {{ font-feature-settings: "tnum" on; }}
</style>
"""


def get_plotly_template():
    return go.layout.Template(
        layout=dict(
            separators=",.",   # vírgula decimal, ponto milhar (pt-BR)
            font=dict(
                family="Inter, -apple-system, sans-serif",
                size=12,
                color=COLORS["ink"],
            ),
            title=dict(
                font=dict(family="Inter, -apple-system, sans-serif", size=14, color=COLORS["ink"]),
                x=0.0, xanchor="left", y=0.97, yanchor="top",
                pad=dict(b=10),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            colorway=[
                COLORS["verde"], COLORS["info"], COLORS["amarelo"],
                COLORS["alerta"], COLORS["verde_med"], COLORS["text_muted"],
                "#7C3AED", "#0891B2",
            ],
            xaxis=dict(
                gridcolor=COLORS["linha"],
                gridwidth=1,
                showline=False, zeroline=False, ticks="",
                tickfont=dict(size=11, color=COLORS["text"]),
                title=dict(font=dict(size=12, color=COLORS["text"]), standoff=10),
                showspikes=False,
            ),
            yaxis=dict(
                gridcolor=COLORS["linha"],
                gridwidth=1,
                showline=False, zeroline=False, ticks="",
                tickfont=dict(size=11, color=COLORS["text"]),
                title=dict(font=dict(size=12, color=COLORS["text"]), standoff=10),
                showspikes=False,
            ),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(0,0,0,0)",
                borderwidth=0,
                font=dict(size=11, color=COLORS["text"]),
                orientation="h",
                yanchor="bottom", y=1.02,
                xanchor="right", x=1,
            ),
            hoverlabel=dict(
                bgcolor=COLORS["ink"],
                font=dict(family="Inter", size=12, color="#FFFFFF"),
                bordercolor=COLORS["ink"],
            ),
            margin=dict(l=50, r=20, t=50, b=40),
        )
    )


_template_registered = False


def apply():
    global _template_registered
    st.markdown(_build_css(), unsafe_allow_html=True)
    if not _template_registered:
        pio.templates["clean"] = get_plotly_template()
        pio.templates.default = "clean"
        _template_registered = True


def header(titulo, subtitulo=None, pill=None, eyebrow="Análise SES-GO"):
    """Header de página interna — pequeno eyebrow + título grande + subtítulo."""
    pill_html = f'<span class="clean-pill">{pill}</span>' if pill else ""
    sub_html = f'<p class="clean-subtitle">{subtitulo}</p>' if subtitulo else ""
    eye_html = f'<div class="clean-eyebrow">{eyebrow}</div>' if eyebrow else ""
    st.markdown(
        f'''
<div class="clean-header">
    {eye_html}
    <h1 class="clean-title">{titulo}{pill_html}</h1>
    {sub_html}
</div>
''',
        unsafe_allow_html=True,
    )


def hero(titulo, subtitulo, meta=None, eyebrow="Análise das OSS · Estado de Goiás"):
    """Hero para a home — header rico com gradiente verde Goiás.

    `meta` é lista de tuplas (label, value) exibidas em linha abaixo do título.
    """
    meta_html = ""
    if meta:
        items = "".join(
            f'<div class="hub-hero-meta-item"><span class="hub-hero-meta-label">{lab}</span><span class="hub-hero-meta-value">{val}</span></div>'
            for lab, val in meta
        )
        meta_html = f'<div class="hub-hero-meta">{items}</div>'
    st.markdown(
        f'''
<div class="hub-hero">
    <div class="hub-hero-eyebrow">{eyebrow}</div>
    <h1 class="hub-hero-title">{titulo}</h1>
    <p class="hub-hero-subtitle">{subtitulo}</p>
    {meta_html}
</div>
''',
        unsafe_allow_html=True,
    )

"""Funções compartilhadas pelos painéis do dashboard."""
import os
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# Allow theme.py to be imported from this directory
sys.path.insert(0, str(Path(__file__).parent))
import theme

# Resolve data dirs: env var > path local (Windows) > path relativo ao projeto
_DEFAULT_LOCAL = Path(r"C:\OSS-Goias\_extractions\_consolidado")
_REPO_ROOT = Path(__file__).resolve().parent.parent  # raiz do repo
_REPO_DATA = _REPO_ROOT / "_extractions" / "_consolidado"

if os.environ.get("OSS_DATA_DIR"):
    CONSOLIDADO_DIR = Path(os.environ["OSS_DATA_DIR"])
elif _DEFAULT_LOCAL.exists():
    CONSOLIDADO_DIR = _DEFAULT_LOCAL
else:
    CONSOLIDADO_DIR = _REPO_DATA

ANALISE_DIR = CONSOLIDADO_DIR / "_analise"

# Re-export institutional palette from theme module
COLORS = theme.COLORS
OSS_COLORS = theme.OSS_COLORS
SCALE_VERDE = theme.SCALE_VERDE
SCALE_EXEC = theme.SCALE_EXEC
SCALE_VERMELHO = theme.SCALE_VERMELHO
SCALE_DOURADO = theme.SCALE_DOURADO
header = theme.header
hero = theme.hero

# ─── Recorte oficial da análise ─────────────────────────────────────────────
# Hospitais e período cobertos pela análise. Aplicado globalmente nas funções
# load_*. CORA / Hospital de Amor está em fase pré-operacional — excluído.
ANO_INICIO = 2023
ANO_FIM = 2026
HOSPITAIS_EXCLUIDOS = {"CORA"}   # pré-operacional
OSS_EXCLUIDAS = {"Hospital de Amor", "Hospital de Amor (CORA)"}

def _apply_scope(df, hospital_col="hospital", oss_col="oss", ano_col="ano"):
    """Aplica filtro do recorte oficial (período 2023-2026 e exclusão de CORA)."""
    if df is None or df.empty: return df
    if hospital_col in df.columns:
        df = df[~df[hospital_col].isin(HOSPITAIS_EXCLUIDOS)]
    if oss_col in df.columns:
        df = df[~df[oss_col].isin(OSS_EXCLUIDAS)]
    if ano_col in df.columns:
        df = df[(pd.to_numeric(df[ano_col], errors="coerce") >= ANO_INICIO) &
                (pd.to_numeric(df[ano_col], errors="coerce") <= ANO_FIM)]
    return df


@st.cache_data(ttl=300)
def load_fato():
    df = pd.read_csv(ANALISE_DIR / "fato_hospital_mes.csv")
    # Coerce numéricos
    for col in df.columns:
        if col in ("hospital", "oss", "ano_mes"): continue
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["data"] = pd.to_datetime(df["ano_mes"] + "-01", errors="coerce")
    return _apply_scope(df)

@st.cache_data(ttl=300)
def load_dim_hospital():
    return pd.read_csv(ANALISE_DIR / "dim_hospital.csv")

@st.cache_data(ttl=300)
def load_cobertura():
    df = pd.read_csv(ANALISE_DIR / "cobertura_kpi.csv")
    return df[~df["hospital"].isin(HOSPITAIS_EXCLUIDOS)]

@st.cache_data(ttl=300)
def load_outliers():
    df = pd.read_csv(ANALISE_DIR / "outliers.csv")
    df = df[~df["hospital"].isin(HOSPITAIS_EXCLUIDOS)] if "hospital" in df.columns else df
    return _apply_scope(df, ano_col="ano") if "ano" in df.columns else df

@st.cache_data(ttl=300)
def load_producao_vs_meta():
    df = pd.read_csv(CONSOLIDADO_DIR / "producao_vs_meta.csv")
    df["realizado"] = pd.to_numeric(df["realizado"], errors="coerce")
    df["meta"] = pd.to_numeric(df["meta"], errors="coerce")
    df["perc_atingimento"] = pd.to_numeric(df["perc_atingimento"], errors="coerce")
    return _apply_scope(df, oss_col="oss_gestora", ano_col="periodo.ano")

@st.cache_data(ttl=300)
def load_categorias_gasto():
    df = pd.read_csv(CONSOLIDADO_DIR / "categorias_gasto.csv")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["perc_total"] = pd.to_numeric(df["perc_total"], errors="coerce")
    return _apply_scope(df, oss_col="oss_gestora", ano_col="periodo.ano")

@st.cache_data(ttl=300)
def load_contratos():
    df = pd.read_csv(CONSOLIDADO_DIR / "contrato_gestao.csv")
    return _apply_scope(df, oss_col="oss_gestora", ano_col="_ano_pasta")

def fmt_brl(v, decimals=0):
    if v is None or pd.isna(v): return "-"
    fmt = f"R$ {{:,.{decimals}f}}".format(v)
    return fmt.replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_brl_short(v):
    """Formato compacto: R$ 1,2 bi / R$ 234 mi / R$ 56 mil."""
    if v is None or pd.isna(v): return "-"
    av = abs(v)
    if av >= 1e9:   return f"R$ {v/1e9:.2f} bi".replace(".", ",")
    if av >= 1e6:   return f"R$ {v/1e6:.1f} mi".replace(".", ",")
    if av >= 1e3:   return f"R$ {v/1e3:.0f} mil"
    return f"R$ {v:.0f}"

def axis_currency_brl(fig, axis="y", short=True):
    """Aplica formatação pt-BR ao eixo de um Plotly figure.
    short=True usa sufixo 'mi'/'bi' (mais legível em gráficos).
    """
    cfg = dict(
        tickprefix="R$ ",
        separatethousands=True,
    )
    if short:
        # 1e9 → "1,2 bi", 1e6 → "60 mi" — usa SI prefix com correção depois
        cfg["tickformat"] = "~s"
        cfg["ticksuffix"] = ""
    else:
        cfg["tickformat"] = ",.0f"
    if axis == "y":
        fig.update_yaxes(**cfg)
    else:
        fig.update_xaxes(**cfg)
    return fig

def fmt_pct(v, decimals=1):
    if v is None or pd.isna(v): return "-"
    return f"{v:.{decimals}f}%"

def get_api_key():
    """Resolve a chave Anthropic em ordem: env var > st.secrets > arquivo local."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    try:
        k = st.secrets.get("anthropic_api_key")
        if k:
            os.environ["ANTHROPIC_API_KEY"] = k
            return k
    except Exception:
        pass
    key_file = Path(r"C:\OSS-Goias\.api-key")
    if key_file.exists():
        k = key_file.read_text(encoding="utf-8").strip()
        os.environ["ANTHROPIC_API_KEY"] = k
        return k
    return None

def setup_page(title, icon="📊"):
    st.set_page_config(
        page_title=f"OSS Goiás · {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    theme.apply()
    # Gate de senha — ativo apenas se dashboard_password estiver em st.secrets
    from auth import require_auth
    require_auth()

"""Gate de senha simples baseado em st.secrets.

Se `dashboard_password` não estiver definida em secrets, o gate é desativado
(acesso livre). Útil para desenvolvimento local sem senha e produção com senha.

Uso: chame `require_auth()` no início de cada página, logo após setup_page().
"""
import streamlit as st


def _get_password():
    try:
        return st.secrets.get("dashboard_password")
    except Exception:
        return None


def require_auth():
    pwd_required = _get_password()
    if not pwd_required:
        return  # sem senha configurada — acesso livre

    if st.session_state.get("auth_ok"):
        return

    # Bloqueia a página e renderiza tela de login centralizada
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }
        .main .block-container { max-width: 420px !important; padding-top: 6rem !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 0.75rem; color: #0D703E; font-weight: 600;
                        letter-spacing: 0.08em; text-transform: uppercase;">
                Secretaria de Estado da Saúde · Goiás
            </div>
            <h1 style="font-size: 1.5rem; font-weight: 700; color: #0F172A;
                       margin: 0.5rem 0 0.5rem 0; letter-spacing: -0.02em;">
                Painel de Auditoria das OSS
            </h1>
            <p style="font-size: 0.9rem; color: #4B5563; margin: 0;">
                Acesso restrito · informe a senha de acesso
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("auth", clear_on_submit=False):
        pwd = st.text_input("Senha", type="password", label_visibility="collapsed",
                            placeholder="Senha de acesso")
        submit = st.form_submit_button("Entrar", use_container_width=True, type="primary")

    if submit:
        if pwd == pwd_required:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")

    st.stop()

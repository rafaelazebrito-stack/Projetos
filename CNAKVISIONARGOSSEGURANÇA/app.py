import streamlit as st
import os
import sys
import json
from datetime import datetime

# ==============================================================================
# 1. NÚCLEO E CONFIGURAÇÃO (ESTRUTURA LIMPA PARA ANÁLISE)
# ==============================================================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Configuração de Página (DEVE SER O PRIMEIRO COMANDO STREAMLIT)
st.set_page_config(
    page_title="CNAK VISION | ARGOS",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# Importação Segura de Módulos
try:
    from componentes.camera import capturar_face
    from banco_dados.database import DatabaseHandler
    from banco_dados.login import carregar_logins
    
    import modulos.cadastro as cadastro
    import modulos.analytics as analytics
    import modulos.seguranca as seguranca
    import modulos.gestao as gestao
    import modulos.marketplace as marketplace
except ImportError as e:
    st.error(f"❌ Erro de Módulo: {e}")
    st.stop()

# Caminhos de Dados
LOGIN_FILE = os.path.join(ROOT_DIR, "cadastros_usuarios", "login_users.json")
RELATORIOS_DIR = os.path.join(ROOT_DIR, "relatorios")
DB_FILE = os.path.join(ROOT_DIR, "cadastros_usuarios", "db_vision_final.csv")
FOTO_DIR = os.path.join(ROOT_DIR, "photos")

# Inicialização de Banco de Dados
db_handler = DatabaseHandler(DB_FILE, ['Nome', 'Documento', 'Email', 'Tipo', 'Foto'])

# ==============================================================================
# 2. DESIGN HUD (CORES MODERNAS E EFEITOS LUMINOSOS)
# ==============================================================================
def aplicar_identidade_visual():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Share+Tech+Mono&display=swap');

        /* Background Carbono e Remoção de Rolagem */
        .stApp {
            background: #0A0A0A !important;
            color: #E0E0E0 !important;
            overflow: hidden;
        }

        /* Título Cnak Vision com Brilho Tático */
        .cyber-header {
            font-family: 'Audiowide', cursive !important;
            font-size: clamp(35px, 7vw, 75px) !important;
            color: #FFD700 !important;
            text-align: center;
            letter-spacing: 12px;
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            margin-bottom: 5px;
            margin-top: -30px;
        }

        /* Painel de Login (Glassmorphism Moderno) */
        .login-card {
            background: rgba(20, 20, 20, 0.9);
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-left: 5px solid #FFD700;
            padding: 30px;
            backdrop-filter: blur(10px);
            border-radius: 4px;
        }

        /* Botões com Efeito de Luz ao passar o mouse (Hover Glow) */
        div.stButton > button {
            background: transparent !important;
            color: #FFD700 !important;
            border: 1px solid #FFD700 !important;
            font-family: 'Share Tech Mono', monospace !important;
            transition: all 0.3s ease !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
        }
        div.stButton > button:hover {
            background: #FFD700 !important;
            color: #000 !important;
            box-shadow: 0 0 35px #FFD700 !important;
            transform: scale(1.02);
        }

        /* Inputs Estilo Terminal */
        input {
            background-color: #151515 !important;
            color: #FFD700 !important;
            border: 1px solid #333 !important;
            font-family: 'Share Tech Mono', monospace !important;
        }
        input:hover { border: 1px solid #FFD700 !important; }

        /* Ocultar UI Padrão */
        header, footer, .stDeployButton {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. INTERFACE DE AUTENTICAÇÃO
# ==============================================================================
def interface_login():
    aplicar_identidade_visual()
    st.markdown('<h1 class="cyber-header">Cnak Vision</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#FFD700; font-family:monospace; margin-top:-15px; opacity:0.6;">SISTEMA OPERACIONAL ARGOS // SESSÃO CRIPTOGRAFADA</p>', unsafe_allow_html=True)
    
    _, col_login, _ = st.columns([1, 1.3, 1])
    with col_login:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        tab_key, tab_bio = st.tabs(["🔑 ACESSO_CHAVE", "📡 BIO_SCANNER"])
        
        with tab_key:
            st.write("### LOGIN PROTOCOL")
            u_id = st.text_input("IDENTIFICADOR", key="usr")
            u_pw = st.text_input("CHAVE_SEGURANCA", type="password", key="pwd")
            
            if st.button("EXECUTAR ACESSO", use_container_width=True):
                # Busca segura no dicionário de logins
                usuario = next((v for v in st.session_state.auth_data.values() if v['id'] == u_id and v['chave'] == u_pw), None)
                if usuario:
                    if usuario.get('status') == "Bloqueado":
                        st.error("⛔ ACESSO NEGADO: OPERADOR SUSPENSO")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user = usuario
                        seguranca.registrar_log(f"LOGIN: {usuario['nome']} autenticado.", RELATORIOS_DIR)
                        st.rerun()
                else:
                    st.error("❌ ERRO: CREDENCIAIS INVÁLIDAS")

        with tab_bio:
            st.write("### NEURAL SCAN")
            foto_bio = capturar_face("cam_main_login", label_botao="Cadastrar Biometria Facial")
            if st.button("RUN SCANNER", use_container_width=True) and foto_bio:
                st.info("Processando padrões faciais...")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. AMBIENTE OPERACIONAL (PÓS-LOGIN)
# ==============================================================================
def ambiente_operacional():
    aplicar_identidade_visual()
    
    with st.sidebar:
        st.markdown(f"### 🛡️ OPERADOR: \n**{st.session_state.user['nome'].upper()}**")
        st.caption(f"Nível: {st.session_state.user.get('nivel')}")
        st.divider()

        modulos_disponiveis = [
            "📝 Cadastro Geral", "📊 BI & Analytics", "🎥 Monitoramento Vídeo",
            "👤 Gestão de Usuários", "📋 Auditoria & Logs", "💎 Mercado"
        ]
        
        # Filtro de permissão por nível
        if st.session_state.user.get('nivel') != "Administrador":
            permissoes = st.session_state.user.get('areas', ["📝 Cadastro Geral"])
            modulos_disponiveis = [m for m in modulos_disponiveis if m in permissoes]

        escolha = st.radio("SISTEMAS ATIVOS:", modulos_disponiveis)
        
        st.divider()
        if st.button("SAIR DO SISTEMA", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # Roteamento de Módulos (Sem perda de funcionalidade)
    if escolha == "📝 Cadastro Geral":
        cadastro.exibir_cadastro(db_handler, FOTO_DIR)
    elif escolha == "📊 BI & Analytics":
        analytics.exibir_bi(db_handler)
    elif escolha == "🎥 Monitoramento Vídeo":
        seguranca.exibir_monitoramento(db_handler, RELATORIOS_DIR)
    elif escolha == "👤 Gestão de Usuários":
        gestao.exibir_gestao(st.session_state.auth_data, LOGIN_FILE)
    elif escolha == "📋 Auditoria & Logs":
        seguranca.exibir_auditoria(RELATORIOS_DIR)
    elif escolha == "💎 Mercado":
        marketplace.exibir_marketplace()

# ==============================================================================
# 5. CONTROLE DE FLUXO PRINCIPAL
# ==============================================================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'auth_data' not in st.session_state:
    st.session_state.auth_data = carregar_logins(LOGIN_FILE)

if not st.session_state.logged_in:
    interface_login()
else:
    ambiente_operacional()
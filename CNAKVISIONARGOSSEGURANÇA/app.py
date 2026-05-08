import streamlit as st
import os
import sys
import json
from datetime import datetime

# ==============================================================================
# 1. CORE ENGINE (Sincronizado e Blindado)
# ==============================================================================
# Ajustando caminhos para o VS Code e Python
caminho_projeto = os.path.dirname(os.path.abspath(__file__))
if caminho_projeto not in sys.path:
    sys.path.insert(0, caminho_projeto)

# Importando módulos de visão cibernética do seu projeto
try:
    from componentes.design import aplicar_design_argos
    from componentes.camera import capturar_face
    from banco_dados.database import DatabaseHandler
    from banco_dados.login import carregar_logins
    
    import modulos.cadastro as cadastro
    import modulos.analytics as analytics
    import modulos.seguranca as seguranca
    import modulos.gestao as gestao
    import modulos.marketplace as marketplace
except ImportError as e:
    st.error(f"⚠️ Erro Crítico de Módulo: {e}")
    st.stop()

# Caminhos de Arquivos de Dados
LOGIN_FILE = os.path.join(caminho_projeto, "cadastros_usuarios", "login_users.json")
RELATORIOS_DIR = os.path.join(caminho_projeto, "relatorios")
DB_FILE = os.path.join(caminho_projeto, "cadastros_usuarios", "db_vision_final.csv")
FOTO_DIR = os.path.join(caminho_projeto, "photos")

# Inicialização do Streamlit com Modo Escuro Nativo
st.set_page_config(page_title="CNAK VISION | ARGOS", layout="wide", page_icon="🛡️")

if 'auth_data' not in st.session_state:
    st.session_state.auth_data = carregar_logins(LOGIN_FILE)

# Manipulador de Banco de Dados CSV
db_handler = DatabaseHandler(DB_FILE, ['Nome', 'Documento', 'Email', 'Tipo', 'Foto'])

# ==============================================================================
# 2. TELA DE LOGIN: ARQUITETURA ARGOS CYBER-COMPACT
# ==============================================================================
def tela_login():
    # Injeção de CSS para condensar a tela e adicionar brilho tático (sem rolling bar)
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Share+Tech+Mono&display=swap');

        /* 2. CONDENSAÇÃO DE TELA: Remove rolagem e centraliza */
        .stApp {
            background: #000;
            /* Efeito de Scanner de Dados no Background */
            background-image: 
                radial-gradient(circle at 50% 50%, rgba(255, 215, 0, 0.05) 0%, transparent 80%),
                linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
                linear-gradient(90deg, rgba(255, 215, 0, 0.015) 1px, transparent 1px),
                linear-gradient(rgba(255, 215, 0, 0.015) 1px, transparent 1px);
            background-size: 100% 100%, 100% 3px, 30px 30px, 30px 30px;
            
            /* Remove a barra de rolagem */
            overflow: hidden; 
            height: 100vh;
            width: 100vw;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* 1. RETIRADA DA IMAGEM PRETA (CONTAINER DO TÍTULO) */
        /* Re-estilizando o título 'Cnak Vision' para ficar fixo e sem container preto */
        .cyber-title {
            font-family: 'Audiowide', cursive !important;
            font-size: 80px !important; /* Tamanho reduzido para compactação */
            color: #FFD700 !important;
            letter-spacing: 12px;
            text-transform: uppercase;
            text-align: center;
            
            /* Efeito Glitch de Descriptografia Tática */
            text-shadow: 2px 2px #ff0000, -2px -2px #0000ff, 0 0 15px rgba(255, 215, 0, 0.6);
            animation: descrypt-glitch 0.2s infinite;
            margin-bottom: 5px; /* Compactando espaço */
        }

        @keyframes descrypt-glitch {
            0% { transform: skew(0.2deg); opacity: 0.8; }
            100% { transform: skew(-0.2deg); opacity: 1; }
        }

        /* Status de Scanner Tático */
        .scanner-status {
            font-family: 'Share Tech Mono', monospace;
            color: #FFD700;
            font-size: 11px;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-align: center;
            opacity: 0.7;
            margin-top: -15px; /* Traz para perto do título */
            margin-bottom: 15px;
        }

        /* 2. CONDENSAÇÃO: Painel de Login Compacto */
        .tactical-panel {
            background: rgba(10, 10, 10, 0.95);
            border-left: 4px solid #FFD700;
            border-right: 1px solid rgba(255, 215, 0, 0.2);
            border-top: 1px solid rgba(255, 215, 0, 0.2);
            border-bottom: 1px solid rgba(255, 215, 0, 0.2);
            padding: 25px; /* Reduzido padding */
            box-shadow: -15px 0 40px rgba(255, 215, 0, 0.1);
            backdrop-filter: blur(10px);
            max-height: 70vh; /* Garante que caiba na tela */
            overflow-y: auto; /* Se houver erro, a rolagem fica no painel, não na tela */
        }

        /* Estilo Tático para Inputs */
        input {
            background-color: #050505 !important;
            border: 1px solid #333 !important;
            color: #FFD700 !important;
            font-family: 'Share Tech Mono', monospace !important;
            height: 35px !important; /* Compactando inputs */
        }

        /* 3. EFEITOS LUMINOSOS AO PASSAR O CURSOR (HOVER GLOOW) */
        /* Brilho Tático nos Inputs de texto */
        input:hover {
            border: 1px solid #FFD700 !important;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.5) !important;
        }

        /* Botão de Acesso Militar com Brilho Tático */
        div.stButton > button {
            background: #FFD700 !important;
            color: #000 !important;
            font-family: 'Audiowide', cursive !important;
            font-size: 16px !important;
            height: 45px !important; /* Compactando botão */
            border: none !important;
            clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%);
            transition: all 0.3s ease !important;
            position: relative;
            overflow: hidden;
        }

        /* EFEITO LUMINOSO (HOVER) DO BOTÃO */
        div.stButton > button:hover {
            background: #fff !important; /* Muda para branco para contraste */
            box-shadow: 0 0 35px #FFD700 !important;
            transform: scale(1.02); /* Leve aumento de tamanho */
            color: #000 !important;
        }

        /* Texto de Protocolo Compacto */
        h3 {
            font-size: 18px !important;
            margin-top: 10px !important;
            margin-bottom: 5px !important;
        }

        /* Condensando as Abas (Tabs) */
        button[data-baseweb="tab"] {
            padding-left: 10px !important;
            padding-right: 10px !important;
            padding-top: 5px !important;
            padding-bottom: 5px !important;
            font-size: 12px !important;
        }

        /* Escondendo elementos de Deploy do Streamlit para imersão total */
        header, footer, .stDeployButton {visibility: hidden;}
        </style>
        
        <h1 class="cyber-title">Cnak Vision</h1>
        <p class="scanner-status">NETWORK_SCAN... ENCRYPTION: AES-256... STATUS: ACTIVE</p>
    """, unsafe_allow_html=True)

    # Centralizando o painel de comando compacto
    _, col_tatico, _ = st.columns([1, 1.4, 1])
    
    with col_tatico:
        st.markdown('<div class="tactical-panel">', unsafe_allow_html=True)
        tab_key, tab_bio = st.tabs(["🔑 KEY_ACCESS", "⚡ BIOMETRIC_SCAN"])
        
        with tab_key:
            st.write("### PROTOCOLO DE LOGIN")
            u_name = st.text_input("ID OPERADOR", key="login_id_compact")
            u_pass = st.text_input("CHAVE DE SEGURANÇA", type="password", key="login_pw_compact")
            
            # O botão já tem a estilização de brilho ao passar o mouse definida no CSS acima
            if st.button("EXECUTE SYSTEM ACCESS", use_container_width=True):
                # Lógica de login (Sincronizada com o banco_dados.login)
                user = next((v for v in st.session_state.auth_data.values() if v['id'] == u_name and v['chave'] == u_pass), None)
                if user:
                    if user.get('status') == "Bloqueado":
                        st.error("⛔ ACCESS DENIED: ACCOUNT SUSPENDED")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        seguranca.registrar_log(f"AUTHORIZED: {user['nome']} entered system.", RELATORIOS_DIR)
                        st.rerun()
                else:
                    st.error("❌ ERROR: INVALID OPERATOR CREDENTIALS")

        with tab_bio:
            st.write("### NEURAL SCANNER")
            # Chama seu componente de câmera tático
            img_cap = capturar_face("neural_scan_v1", label_botao="Cadastrar Biometria Facial")
            if st.button("RUN SCAN", use_container_width=True) and img_cap:
                st.warning("ANALYZING BIOMETRIC NODES...")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 3. HUB DE COMANDO CENTRAL (MENU PÓS-LOGIN)
# ==============================================================================
if not st.session_state.get('logged_in', False):
    tela_login()
else:
    # Sidebar Estilo Terminal
    st.sidebar.markdown(f"### 📡 OPERADOR: {st.session_state.user['nome'].upper()}")
    st.sidebar.write(f"SYSTEM_LEVEL: {st.session_state.user.get('nivel')}")
    
    # Nomes dos módulos atualizados (Sincronizado com o seguranca.py)
    modulos = [
        "📝 Cadastro Geral", 
        "📊 BI & Analytics", 
        "🎥 Monitoramento Vídeo",
        "👤 Gestão de Usuários", 
        "📋 Auditoria & Logs", # Nome exato para roteamento
        "💎 Mercado"
    ]
    
    # Lógica de Permissão baseada no nível (Sincronizado com login.py)
    if st.session_state.user.get('nivel') == "Administrador":
        opcoes = modulos
    else:
        # Se for atendente, usa a lista de áreas permitidas do JSON
        permissoes = st.session_state.user.get('areas', ["📝 Cadastro Geral"])
        opcoes = [m for m in modulos if m in permissoes]

    menu = st.sidebar.radio("SISTEMAS_ATIVOS:", opcoes)
    
    st.sidebar.divider()
    if st.sidebar.button("TERMINATE_SESSION"):
        st.session_state.logged_in = False
        st.rerun()

    # Roteamento dos Módulos (Garantindo que o seguranca.registrar_log funcione)
    if menu == "📝 Cadastro Geral":
        seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou no Cadastro Geral.", RELATORIOS_DIR)
        cadastro.exibir_cadastro(db_handler, FOTO_DIR)
    elif menu == "📊 BI & Analytics":
        seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou no BI & Analytics.", RELATORIOS_DIR)
        analytics.exibir_bi(db_handler)
    elif menu == "🎥 Monitoramento Vídeo":
        seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou no Monitoramento Vídeo.", RELATORIOS_DIR)
        seguranca.exibir_monitoramento(db_handler, RELATORIOS_DIR)
    elif menu == "👤 Gestão de Usuários":
        # Nota: app.py registra logs aqui conforme sua estrutura anterior
        seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou na Gestão de Acessos.", RELATORIOS_DIR)
        gestao.exibir_gestao(st.session_state.auth_data, LOGIN_FILE)
    elif menu == "📋 Auditoria & Logs":
        seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou na Auditoria.", RELATORIOS_DIR)
        seguranca.exibir_auditoria(RELATORIOS_DIR)
    elif menu == "💎 Mercado":
        seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou no Marketplace.", RELATORIOS_DIR)
        marketplace.exibir_marketplace()
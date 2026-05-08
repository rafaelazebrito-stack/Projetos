import streamlit as st
import os
import sys
import json
from datetime import datetime

# ==============================================================================
# 1. CONFIGURAÇÃO DE AMBIENTE E IMPORTAÇÕES
# ==============================================================================
caminho_projeto = os.path.dirname(os.path.abspath(__file__))
if caminho_projeto not in sys.path:
    sys.path.insert(0, caminho_projeto)

try:
    from componentes.design import aplicar_design_argos
    from componentes.camera import capturar_face, salvar_foto
    from banco_dados.database import DatabaseHandler
    from banco_dados.login import carregar_logins, salvar_login
    
    import modulos.cadastro as cadastro
    import modulos.analytics as analytics
    import modulos.seguranca as seguranca
    import modulos.gestao as gestao
    import modulos.marketplace as marketplace
except ImportError as e:
    st.error(f"Erro Crítico de Módulo: {e}")
    st.stop()

# 2. CONFIGURAÇÃO DE DIRETÓRIOS
DB_FILE = os.path.join(caminho_projeto, "cadastros_usuarios", "db_vision_final.csv")
LOGIN_FILE = os.path.join(caminho_projeto, "cadastros_usuarios", "login_users.json")
FOTO_DIR = os.path.join(caminho_projeto, "photos")
RELATORIOS_DIR = os.path.join(caminho_projeto, "relatorios")

for p in [FOTO_DIR, RELATORIOS_DIR]:
    os.makedirs(p, exist_ok=True)

COLUNAS = ['Nome', 'Documento', 'Email', 'Telefone', 'Tipo', 'Sexo', 'Endereco', 'Origem', 'Data_Cad', 'Foto']

# Inicialização da Página
st.set_page_config(page_title="CNAK VISION", layout="wide", page_icon="🛡️")
aplicar_design_argos()

if 'auth_data' not in st.session_state:
    st.session_state.auth_data = carregar_logins(LOGIN_FILE)

db_handler = DatabaseHandler(DB_FILE, COLUNAS)

# ==============================================================================
# 3. TELA DE LOGIN (COM MOVIMENTO E BIOMETRIA ARGOS)
# ==============================================================================
def tela_login():
    st.markdown('<div class="login-anim">', unsafe_allow_html=True)
    st.markdown('<h1 class="titulo-neon">CNAK VISION</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tecnologia-credito">TECNOLOGIA DESENVOLVIDA POR ARGOS SEGURANÇA</p>', unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        tab_senha, tab_facial = st.tabs(["🔐 Senha", "👤 Face"])
        with tab_senha:
            user_id = st.text_input("Usuário", key="input_user")
            senha = st.text_input("Senha", type="password", key="input_pass")
            if st.button("ACESSAR SISTEMA", use_container_width=True):
                user = next((v for v in st.session_state.auth_data.values() if v['id'] == user_id and v['chave'] == senha), None)
                if user:
                    if user.get('status') == "Bloqueado":
                        st.error("ACESSO NEGADO: Este usuário está bloqueado.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        seguranca.registrar_log(f"LOGIN: {user['nome']} acessou o sistema.", RELATORIOS_DIR)
                        st.rerun()
                else: st.error("Credenciais Inválidas.")
        with tab_facial:
            face_data = capturar_face("login")
            if st.button("AUTENTICAR FACE", use_container_width=True) and face_data:
                # Simulação para login facial
                user = list(st.session_state.auth_data.values())[0]
                st.session_state.logged_in = True
                st.session_state.user = user
                seguranca.registrar_log(f"LOGIN: {user['nome']} acessou via BIOMETRIA.", RELATORIOS_DIR)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. HUB PRINCIPAL (COM FILTRO DE PERMISSÕES)
# ==============================================================================
if not st.session_state.get('logged_in', False):
    tela_login()
else:
    # Sidebar: Identificação do Operador
    st.sidebar.markdown(f"### 🛡️ OPERADOR: {st.session_state.user['nome'].upper()}")
    st.sidebar.markdown(f"**Nível:** {st.session_state.user.get('nivel', 'Acesso Restrito')}")

    # LÓGICA DE CONTROLE DE ACESSO (O PONTO QUE VOCÊ SOLICITOU)
    lista_mestra_modulos = [
        "📝 Cadastro Geral", 
        "📊 BI & Analytics", 
        "🎥 Monitoramento Vídeo",
        "👤 Gestão de Usuários", 
        "📋 Auditoria & Logs",
        "💎 Marketplace"
    ]
    
    # 1. Recupera as áreas permitidas do cadastro do usuário
    areas_permitidas = st.session_state.user.get('areas', ["📝 Cadastro Geral"])
    
    # 2. Filtra o menu: Administrador vê tudo, outros veem apenas o que foi marcado no cadastro
    if st.session_state.user.get('nivel') == "Administrador":
        modulos_disponiveis = lista_mestra_modulos
    else:
        modulos_disponiveis = [m for m in lista_mestra_modulos if m in areas_permitidas]

    # 3. Gera o rádio apenas com as opções filtradas
    if not modulos_disponiveis:
        st.sidebar.warning("Nenhum módulo autorizado.")
        menu = None
    else:
        menu = st.sidebar.radio("MÓDULOS DISPONÍVEIS:", modulos_disponiveis)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("LOGOUT (SAIR)"):
        seguranca.registrar_log(f"LOGOUT: {st.session_state.user['nome']} saiu.", RELATORIOS_DIR)
        st.session_state.logged_in = False
        st.rerun()

    # Roteamento Seguro (Sempre registra no log o acesso)
    if menu:
        if menu == "📝 Cadastro Geral":
            seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou no Cadastro.", RELATORIOS_DIR)
            cadastro.exibir_cadastro(db_handler, FOTO_DIR)
            
        elif menu == "📊 BI & Analytics":
            seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} visualizou Analytics.", RELATORIOS_DIR)
            analytics.exibir_bi(db_handler)
            
        elif menu == "🎥 Monitoramento Vídeo":
            seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} monitorou as câmeras.", RELATORIOS_DIR)
            seguranca.exibir_monitoramento(db_handler, RELATORIOS_DIR)

        elif menu == "👤 Gestão de Usuários":
            seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} entrou na Gestão de Acessos.", RELATORIOS_DIR)
            gestao.exibir_gestao(st.session_state.auth_data, LOGIN_FILE)

        elif menu == "📋 Auditoria & Logs":
            seguranca.exibir_auditoria(RELATORIOS_DIR)

        elif menu == "💎 Marketplace":
            seguranca.registrar_log(f"ACESSO: {st.session_state.user['nome']} visualizou o Marketplace.", RELATORIOS_DIR)
            marketplace.exibir_marketplace()
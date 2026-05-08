import streamlit as st
import json
import os

def exibir_gestao(auth_data, login_file):
    """
    Interface de Gerenciamento de Operadores Argos.
    Removida temporariamente a captura biométrica para simplificação do protocolo.
    """
    st.markdown('<h2 class="glow-text">👤 Gestão de Operadores e Credenciais</h2>', unsafe_allow_html=True)
    
    # --- ABA 1: LISTAGEM DE OPERADORES ATIVOS ---
    tab_lista, tab_novo, tab_config = st.tabs(["📋 Operadores Ativos", "➕ Novo Cadastro", "⚙️ Configurações"])
    
    with tab_lista:
        st.write("### Auditoria de Acessos")
        if auth_data:
            for username, info in auth_data.items():
                with st.expander(f"🔐 {info['nome']} ({info['id']})"):
                    col_info, col_status = st.columns(2)
                    with col_info:
                        st.write(f"**Nível:** {info.get('nivel', 'Atendente')}")
                        st.write(f"**Áreas:** {', '.join(info.get('areas', []))}")
                    with col_status:
                        status = info.get('status', 'Ativo')
                        st.select_slider(
                            f"Status do Operador: {username}",
                            options=["Ativo", "Bloqueado"],
                            value=status,
                            key=f"status_{username}"
                        )
        else:
            st.info("Nenhum operador registrado no sistema.")

    with tab_novo:
        st.write("### Protocolo de Novo Operador")
        with st.form("form_novo_user", clear_on_submit=True):
            n_nome = st.text_input("NOME COMPLETO")
            n_id = st.text_input("ID DE LOGIN (Ex: argos_01)")
            n_pass = st.text_input("CHAVE DE ACESSO", type="password")
            
            n_nivel = st.selectbox("NÍVEL DE AUTORIDADE", ["Administrador", "Segurança", "Atendente"])
            
            st.write("---")
            st.write("**Permissões de Módulo:**")
            check_cad = st.checkbox("📝 Cadastro Geral", value=True)
            check_bi = st.checkbox("📊 BI Analytics")
            check_aud = st.checkbox("📋 Auditoria")
            
            btn_criar = st.form_submit_button("🚀 REGISTRAR OPERADOR")
            
            if btn_criar:
                if n_nome and n_id and n_pass:
                    # Construindo as permissões
                    areas = []
                    if check_cad: areas.append("📝 Cadastro Geral")
                    if check_bi: areas.append("📊 BI Analytics")
                    if check_aud: areas.append("📋 Auditoria")
                    
                    # Novo registro sem o campo de biometria facial
                    auth_data[n_id] = {
                        "nome": n_nome,
                        "id": n_id,
                        "chave": n_pass,
                        "nivel": n_nivel,
                        "status": "Ativo",
                        "areas": areas
                    }
                    
                    # Persistência no JSON
                    try:
                        with open(login_file, "w", encoding="utf-8") as f:
                            json.dump(auth_data, f, indent=4, ensure_ascii=False)
                        st.success(f"✅ Operador {n_nome} integrado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao salvar credenciais: {e}")
                else:
                    st.warning("Preencha todos os campos obrigatórios.")

    with tab_config:
        st.write("### Parâmetros do Sistema")
        st.info("Configurações globais de segurança e tempo de sessão.")
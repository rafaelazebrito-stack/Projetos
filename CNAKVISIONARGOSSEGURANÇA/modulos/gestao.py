import streamlit as st
import json
from componentes.camera import capturar_face

def exibir_gestao(auth_data, login_file):
    st.markdown('<h2 class="glow-text">🛡️ Gestão de Operadores Argos</h2>', unsafe_allow_html=True)
    
    NIVEIS = ["Administrador", "Diretoria", "Lojista", "Segurança", "Atendente"]
    AREAS = ["📝 Cadastro Geral", "📊 BI & Analytics", "🎥 Monitoramento Vídeo", "👤 Gestão de Usuários", "📋 Auditoria & Logs", "💎 Marketplace"]

    tab_listar, tab_novo = st.tabs(["👥 Operadores Habilitados", "➕ Novo Acesso"])

    # --- ABA 1: LISTAR, EDITAR, BIOMETRIA, BLOQUEIO E EXCLUSÃO ---
    with tab_listar:
        if not auth_data:
            st.info("Nenhum operador no sistema.")
        else:
            # Seleção de usuário por Selectbox para garantir que apenas UM formulário 
            # de câmera seja renderizado por vez. Isso mata o erro removeChild.
            uids = list(auth_data.keys())
            selecionado = st.selectbox("Selecione o Operador para Gerenciar:", uids, 
                                     format_func=lambda x: f"{auth_data[x]['nome']} ({x})")
            
            if selecionado:
                info = auth_data[selecionado]
                st.markdown(f"### 👤 Gerenciando: {info['nome']}")
                
                # --- SUB-SEÇÃO: BIOMETRIA (A funcionalidade que você pediu) ---
                with st.expander("📸 Atualizar Biometria Facial", expanded=False):
                    st.write("Capture uma nova face para substituir a atual.")
                    # Key estática garante que o nó do DOM seja fixo
                    nova_face = capturar_face(key_camera="CAM_GESTAO_FIXA", label_botao="Cadastrar Biometria Facial")
                    if st.button("Vincular Nova Face ao Perfil", use_container_width=True):
                        if nova_face:
                            auth_data[selecionado]["foto_biometria"] = nova_face
                            with open(login_file, 'w', encoding='utf-8') as f:
                                json.dump(auth_data, f, indent=4, ensure_ascii=False)
                            st.success("Biometria atualizada!")
                            st.rerun()

                # --- SUB-SEÇÃO: DADOS CADASTRAIS ---
                with st.form(key=f"form_edicao_{selecionado}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        e_nome = st.text_input("Nome Completo", value=info.get('nome'))
                        e_email = st.text_input("E-mail", value=info.get('email', ''))
                    with col2:
                        e_senha = st.text_input("Senha", value=info.get('chave'), type="password")
                        e_nivel = st.selectbox("Nível", NIVEIS, index=NIVEIS.index(info.get('nivel', 'Atendente')) if info.get('nivel') in NIVEIS else 4)
                    
                    e_areas = st.multiselect("Permissões", AREAS, default=info.get('areas', []))
                    
                    if st.form_submit_button("💾 SALVAR ALTERAÇÕES CADASTRAIS"):
                        auth_data[selecionado].update({
                            "nome": e_nome, "email": e_email, "chave": e_senha, "nivel": e_nivel, "areas": e_areas
                        })
                        with open(login_file, 'w', encoding='utf-8') as f:
                            json.dump(auth_data, f, indent=4, ensure_ascii=False)
                        st.success("Dados salvos!")
                        st.rerun()

                # --- SUB-SEÇÃO: STATUS E EXCLUSÃO ---
                st.markdown("---")
                c_status, c_del = st.columns(2)
                with c_status:
                    status_atual = info.get('status', 'Ativo')
                    label_status = "🚫 BLOQUEAR ACESSO" if status_atual == "Ativo" else "✅ REATIVAR ACESSO"
                    if st.button(label_status, use_container_width=True):
                        auth_data[selecionado]['status'] = "Bloqueado" if status_atual == "Ativo" else "Ativo"
                        with open(login_file, 'w', encoding='utf-8') as f:
                            json.dump(auth_data, f, indent=4)
                        st.rerun()
                
                with c_del:
                    if st.button("🗑️ EXCLUIR DEFINITIVAMENTE", use_container_width=True, type="secondary"):
                        del auth_data[selecionado]
                        with open(login_file, 'w', encoding='utf-8') as f:
                            json.dump(auth_data, f, indent=4)
                        st.success("Operador removido.")
                        st.rerun()

    # --- ABA 2: NOVO CADASTRO (FUNCIONALIDADE COMPLETA) ---
    with tab_novo:
        st.write("### 📸 Biometria Facial Obrigatória")
        face_novo = capturar_face(key_camera="CAM_NOVO_FIXA", label_botao="Cadastrar Biometria Facial")
        
        with st.form(key="form_novo_completo"):
            c1, c2 = st.columns(2)
            with c1:
                n_id = st.text_input("Login (ID) *")
                n_nome = st.text_input("Nome Completo *")
                n_email = st.text_input("E-mail")
            with c2:
                n_pass = st.text_input("Senha *", type="password")
                n_nivel = st.selectbox("Nível de Autoridade", NIVEIS)
                n_areas = st.multiselect("Áreas de Acesso", AREAS, default=["📝 Cadastro Geral"])
            
            if st.form_submit_button("🚀 HABILITAR OPERADOR"):
                if n_id and n_nome and n_pass:
                    auth_data[n_id] = {
                        "nome": n_nome, "id": n_id, "chave": n_pass, "email": n_email,
                        "nivel": n_nivel, "areas": n_areas, "status": "Ativo", "foto_biometria": face_novo
                    }
                    with open(login_file, 'w', encoding='utf-8') as f:
                        json.dump(auth_data, f, indent=4, ensure_ascii=False)
                    st.success(f"Operador {n_nome} habilitado com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos com asterisco (*).")
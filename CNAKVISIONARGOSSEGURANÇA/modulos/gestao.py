import streamlit as st
import json
import os
from componentes.camera import capturar_face

def exibir_gestao(auth_data, login_file):
    st.markdown('<h2 class="glow-text">🛡️ Operadores Habilitados Argos</h2>', unsafe_allow_html=True)
    
    NIVEIS_OFICIAIS = ["Administrador", "Diretoria", "Lojista", "Segurança", "Atendente"]
    AREAS_OFICIAIS = ["📝 Cadastro Geral", "📊 BI & Analytics", "🎥 Monitoramento Vídeo", "👤 Gestão de Usuários", "📋 Auditoria & Logs", "💎 Marketplace"]

    tab_listar, tab_novo = st.tabs(["👥 Operadores Habilitados", "➕ Cadastrar Novo"])

    # --- ABA: LISTAR / EDITAR ---
    with tab_listar:
        if not auth_data:
            st.info("Nenhum operador habilitado.")
        else:
            for uid, info in list(auth_data.items()):
                # Usamos o ID do usuário no título para evitar confusão de estado
                with st.container(border=True):
                    st.markdown(f"### 👤 {info['nome'].upper()} ({uid})")
                    
                    # 1. A Câmera fica TOTALMENTE FORA de formulários ou expanders aninhados
                    # Isso evita o erro de removeChild no DOM do navegador
                    st.write("📸 **Biometria Facial**")
                    nova_face = capturar_face(f"cam_fixed_{uid}", label_botao="Cadastrar Biometria Facial")

                    # 2. Formulário apenas para os dados textuais
                    with st.form(key=f"form_ed_safe_{uid}"):
                        c1, c2 = st.columns(2)
                        
                        nivel_atual = info.get('nivel', 'Atendente')
                        idx_nivel = NIVEIS_OFICIAIS.index(nivel_atual) if nivel_atual in NIVEIS_OFICIAIS else 4

                        with c1:
                            edit_nome = st.text_input("Nome Completo", value=info.get('nome'))
                            edit_email = st.text_input("E-mail", value=info.get('email', ''))
                        with c2:
                            edit_senha = st.text_input("Senha", value=info.get('chave'), type="password")
                            edit_nivel = st.selectbox("Nível", NIVEIS_OFICIAIS, index=idx_nivel)

                        edit_areas = st.multiselect("Permissões", AREAS_OFICIAIS, default=info.get('areas', []))

                        if st.form_submit_button("💾 SALVAR DADOS E BIOMETRIA"):
                            # Só atualizamos a foto se uma nova foi tirada, senão mantemos a original
                            foto_final = nova_face if nova_face else info.get('foto_biometria')
                            
                            auth_data[uid] = {
                                "nome": edit_nome,
                                "id": uid,
                                "chave": edit_senha,
                                "email": edit_email,
                                "nivel": edit_nivel,
                                "areas": edit_areas,
                                "status": info.get('status', 'Ativo'),
                                "foto_biometria": foto_final
                            }
                            
                            with open(login_file, 'w', encoding='utf-8') as f:
                                json.dump(auth_data, f, indent=4, ensure_ascii=False)
                            
                            st.success(f"Cadastro de {uid} atualizado!")
                            st.rerun()

                    # Opções de Exclusão/Bloqueio (Botões simples)
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button(f"Bloquear/Ativar {uid}", key=f"btn_st_{uid}"):
                            auth_data[uid]['status'] = "Bloqueado" if info.get('status') == "Ativo" else "Ativo"
                            with open(login_file, 'w', encoding='utf-8') as f:
                                json.dump(auth_data, f, indent=4)
                            st.rerun()
                    with col_b2:
                        if st.button(f"Excluir Acesso {uid}", key=f"btn_del_{uid}"):
                            del auth_data[uid]
                            with open(login_file, 'w', encoding='utf-8') as f:
                                json.dump(auth_data, f, indent=4)
                            st.rerun()
                    st.markdown("---")

    # --- ABA: CADASTRAR NOVO ---
    with tab_novo:
        st.write("### 📸 Captura de Biometria")
        # Fora do form também no cadastro
        face_nova_cadastro = capturar_face("cam_new_safe", label_botao="Cadastrar Biometria Facial")
        
        with st.form("form_novo_v7"):
            c1, c2 = st.columns(2)
            with c1:
                n_nome = st.text_input("Nome Completo *")
                n_id = st.text_input("Login (Usuário) *")
                n_email = st.text_input("E-mail *")
            with c2:
                n_pass = st.text_input("Senha *", type="password")
                n_nivel = st.selectbox("Nível", NIVEIS_OFICIAIS)
                n_areas = st.multiselect("Áreas", AREAS_OFICIAIS, default=["📝 Cadastro Geral"])
            
            if st.form_submit_button("CADASTRAR OPERADOR"):
                if n_nome and n_id and n_pass:
                    auth_data[n_id] = {
                        "nome": n_nome, "id": n_id, "chave": n_pass, "email": n_email,
                        "nivel": n_nivel, "areas": n_areas, "status": "Ativo", "foto_biometria": face_nova_cadastro
                    }
                    with open(login_file, 'w', encoding='utf-8') as f:
                        json.dump(auth_data, f, indent=4, ensure_ascii=False)
                    st.success("Habilitado com Sucesso!")
                    st.rerun()
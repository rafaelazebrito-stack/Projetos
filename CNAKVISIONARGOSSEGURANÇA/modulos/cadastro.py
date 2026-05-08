import streamlit as st
from datetime import datetime
# Importamos as funções diretamente do seu módulo de câmera
from componentes.camera import capturar_face, salvar_foto
from utilitarios.formatadores import Utils

def exibir_cadastro(db_handler, foto_dir):
    st.markdown('<h2 class="glow-text">📝 Registro Central de Visitantes</h2>', unsafe_allow_html=True)
    
    # Iniciando o formulário
    with st.form("form_registro_geral", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *")
            doc = st.text_input("CPF *", placeholder="000.000.000-00")
            email = st.text_input("E-mail *")
        
        with col2:
            tipo = st.selectbox("Tipo de Acesso", ["Diretoria", "Operacional", "Lojista", "Visitante"])
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Não Informado"])
            endereco = st.text_input("Endereço Completo")

        st.markdown("---")
        # Chamada da função de câmera (usando o nome atualizado)
        foto_b64 = capturar_face("cadastro_geral")
        
        # O BOTÃO DE ENVIO (Resolve o erro do Streamlit)
        btn_enviar = st.form_submit_button("REGISTRAR NO SISTEMA ARGOS")

        if btn_enviar:
            if nome and doc and email:
                doc_formatado = Utils.formatar_cpf(doc)
                
                # Verifica duplicidade antes de salvar
                duplicidade = db_handler.is_duplicate(nome, doc_formatado, email)
                
                if duplicidade:
                    st.error(f"ERRO: Cadastro duplicado detectado no campo: {duplicidade}")
                else:
                    # Salva a foto fisicamente
                    caminho_foto = salvar_foto(None, doc_formatado, foto_dir, foto_b64)
                    
                    novo_usuario = {
                        'Nome': nome,
                        'Documento': doc_formatado,
                        'Email': email,
                        'Telefone': "N/A",
                        'Tipo': tipo,
                        'Sexo': sexo,
                        'Endereco': endereco,
                        'Origem': "CNAK Vision",
                        'Data_Cad': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'Foto': caminho_foto
                    }
                    
                    db_handler.save_user(novo_usuario)
                    st.success(f"Cadastro de {nome} realizado com sucesso!")
                    st.rerun()
            else:
                st.warning("Por favor, preencha todos os campos obrigatórios (*).")

    # Galeria de Perfis (Opcional, se quiser ver os registros abaixo do form)
    st.markdown("---")
    st.markdown("### 👥 Galeria de Registros")
    df = db_handler.get_all_users()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
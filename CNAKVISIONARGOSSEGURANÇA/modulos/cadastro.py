import streamlit as st
import os
from componentes.camera import capturar_face
# Importação explícita para evitar o erro de 'nome não encontrado'
from componentes.design import salvar_foto, aplicar_design_argos

def exibir_cadastro(db_handler, foto_dir):
    # Aplica o estilo visual da Argos
    aplicar_design_argos()
    st.markdown('<h2 class="glow-text">📝 Cadastro Geral de Acessos</h2>', unsafe_allow_html=True)
    
    # Formulário Unificado
    with st.form(key="form_cadastro_final", clear_on_submit=True):
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📋 Informações")
            nome = st.text_input("NOME COMPLETO *")
            documento = st.text_input("DOCUMENTO (CPF/RG) *")
            email = st.text_input("E-MAIL")
            
        with c2:
            st.subheader("📸 Identificação")
            tipo = st.selectbox("TIPO DE ACESSO", ["Visitante", "Morador", "Prestador", "Veículo"])
            # Captura da foto via componente de câmera
            foto_b64 = capturar_face("cam_cadastro", label_botao="Capturar Imagem")

        # Botão de ação
        if st.form_submit_button("🚀 FINALIZAR REGISTRO", use_container_width=True):
            if nome and documento:
                id_limpo = documento.replace(".", "").replace("-", "").strip()
                
                # Executa o salvamento da foto e do CSV
                caminho_foto = salvar_foto(id_limpo, foto_dir, foto_b64)
                
                # Payload para o Banco de Dados
                dados = [nome.upper(), documento, email, tipo, caminho_foto]
                db_handler.adicionar_registro(dados)
                
                st.success(f"✅ Protocolo de {nome} arquivado com sucesso!")
            else:
                st.warning("⚠️ Preencha Nome e Documento para continuar.")

    # Área de Auditoria Rápida
    st.divider()
    with st.expander("🔍 Visualizar Últimos Registros"):
        df = db_handler.ler_todos()
        if not df.empty:
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
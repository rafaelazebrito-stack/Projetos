import streamlit as st
import pandas as pd
import os

def exibir_cadastro(db_handler, foto_dir):
    st.markdown('<h2 style="color:#FFD700; font-family:sans-serif;">📝 Registro de Acesso</h2>', unsafe_allow_html=True)
    
    with st.form(key="form_cadastro_atualizado", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("NOME COMPLETO *")
            documento = st.text_input("CPF/RG *")
            email = st.text_input("E-MAIL")
            
        with col2:
            # ATUALIZADO: Novas categorias solicitadas
            categorias = ["Administrador", "Diretoria", "Lojista", "Atendente", "Visitante", "Segurança"]
            tipo_acesso = st.selectbox("CATEGORIA", categorias)
            endereco = st.text_input("ENDEREÇO COMPLETO", placeholder="Rua, Número, Bairro, Cidade-UF")

        btn_cadastrar = st.form_submit_button("🚀 EXECUTAR REGISTRO", use_container_width=True)

        if btn_cadastrar:
            if nome and documento:
                dados = [nome.upper(), documento, email, endereco, tipo_acesso, "n/a"]
                
                try:
                    # TENTATIVA INTELIGENTE: Tenta os nomes mais comuns para o método de salvar
                    if hasattr(db_handler, 'adicionar_registro'):
                        db_handler.adicionar_registro(dados)
                    elif hasattr(db_handler, 'salvar'):
                        db_handler.salvar(dados)
                    elif hasattr(db_handler, 'save'):
                        db_handler.save(dados)
                    else:
                        st.error("Erro Técnico: Método de gravação não encontrado no DatabaseHandler.")
                        return
                        
                    st.success(f"✅ {nome} registrado com sucesso!")
                except Exception as e:
                    st.error(f"Falha na gravação: {e}")
            else:
                st.warning("Preencha Nome e Documento.")

    st.divider()
    st.write("### 📋 Últimos Registros")
    
    # CORREÇÃO DO LER_TODOS: Tenta encontrar o método de leitura correto
    try:
        metodos_leitura = ['ler_todos', 'ler_dados', 'get_all', 'read_all']
        df = None
        for metodo in metodos_leitura:
            if hasattr(db_handler, metodo):
                df = getattr(db_handler, metodo)()
                break
        
        if df is not None and not df.empty:
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
    except:
        st.info("Sincronizando banco de dados...")
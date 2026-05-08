import streamlit as st
import os
import base64

def aplicar_design_argos():
    """Aplica o CSS base de identidade visual Argos."""
    st.markdown("""
        <style>
        .glow-text {
            color: #FFD700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
            font-family: 'Audiowide', sans-serif;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

def salvar_foto(id_foto, diretorio, base64_data):
    """
    Processa e salva uma imagem em Base64 de forma segura.
    Argumentos: ID (Nome do arquivo), Diretorio, Dados da Imagem.
    """
    if not base64_data:
        return "sem_foto.png"

    try:
        # Garante a infraestrutura de pastas
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        # Limpeza do cabeçalho Base64 para evitar corrupção de arquivo
        if "," in base64_data:
            base64_data = base64_data.split(",")[1]

        img_data = base64.b64decode(base64_data)
        nome_arquivo = f"{id_foto}.png"
        caminho_completo = os.path.join(diretorio, nome_arquivo)

        with open(caminho_completo, "wb") as f:
            f.write(img_data)

        return nome_arquivo
    except Exception as e:
        st.error(f"⚠️ Erro Crítico de Mídia: {e}")
        return "erro_foto.png"
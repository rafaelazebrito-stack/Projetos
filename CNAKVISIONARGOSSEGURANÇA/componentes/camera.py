import streamlit as st
import cv2
import PIL.Image as Image
import numpy as np
import base64
import os
from io import BytesIO

def capturar_face(key_camera="default", label_botao="Cadastrar Biometria Facial"):
    """
    Captura a face via webcam, otimiza a imagem com OpenCV para não sobrecarregar 
    o JSON e converte para Base64.
    """
    # O componente do Streamlit agora aceita o nome que você definir
    foto = st.camera_input(label_botao, key=key_camera)
    
    if foto is not None:
        try:
            # 1. Converte o upload do Streamlit para o formato PIL
            img_pil = Image.open(foto)
            
            # 2. Converte para Array NumPy para que o OpenCV (cv2) possa processar
            img_array = np.array(img_pil)
            
            # 3. Converte de RGB (padrão web) para BGR (padrão OpenCV)
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # 4. Redimensionamento Inteligente (Otimização)
            # Mantemos 300x300 para garantir que o reconhecimento facial seja preciso
            # mas o arquivo de banco de dados não fique gigantesco.
            img_resized = cv2.resize(img_cv, (300, 300))
            
            # 5. Codificação para PNG e conversão para Base64 (Texto)
            _, buffer = cv2.imencode('.png', img_resized)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            st.error(f"Erro no processamento da biometria: {e}")
            return None
            
    return None

def salvar_foto(img_str, nome_arquivo, pasta_fotos):
    """
    Salva a string Base64 como um arquivo físico .png na pasta de fotos.
    """
    if img_str:
        try:
            os.makedirs(pasta_fotos, exist_ok=True)
            caminho_completo = os.path.join(pasta_fotos, f"{nome_arquivo}.png")
            
            # Decodifica o texto de volta para imagem
            img_data = base64.b64decode(img_str)
            with open(caminho_completo, "wb") as f:
                f.write(img_data)
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo físico: {e}")
            return False
    return False
import streamlit as st

def aplicar_design_argos():
    """Injeta o CSS profissional da Argos Segurança com efeitos Neon e Movimento."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;600&display=swap');

        /* Configuração do Fundo e Texto */
        .stApp {
            background: radial-gradient(circle at top, #1a1a1a 0%, #000000 100%);
            color: #ffd700;
            font-family: 'Rajdhani', sans-serif;
        }

        /* Animação de Abertura (Item 5 da solicitação) */
        @keyframes aberturaMovimento {
            0% { opacity: 0; transform: translateY(30px); filter: blur(10px); }
            100% { opacity: 1; transform: translateY(0); filter: blur(0); }
        }
        .login-anim {
            animation: aberturaMovimento 1.5s ease-out;
        }

        /* Título Neon com Efeito Especial no Hover (Itens 2 e 4) */
        .titulo-neon {
            font-family: 'Orbitron', sans-serif;
            color: #ffd700;
            text-align: center;
            font-size: 3.5rem;
            letter-spacing: 8px;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
            transition: all 0.5s ease;
            cursor: pointer;
            margin-bottom: 5px;
        }
        .titulo-neon:hover {
            text-shadow: 0 0 20px #ffd700, 0 0 40px #ffd700, 0 0 60px #daa520;
            transform: scale(1.05);
        }

        /* Tecnologia Argos (Item 3) */
        .tecnologia-credito {
            text-align: center;
            font-family: 'Rajdhani', sans-serif;
            color: #ffd700;
            font-size: 0.9rem;
            letter-spacing: 4px;
            font-weight: 600;
            opacity: 0.8;
            margin-bottom: 40px;
            text-transform: uppercase;
        }

        /* Botões Dourados com Neon no Hover (Item 4) */
        .stButton>button {
            background: transparent !important;
            color: #ffd700 !important;
            border: 2px solid #ffd700 !important;
            border-radius: 4px !important;
            padding: 10px 25px !important;
            font-family: 'Orbitron', sans-serif !important;
            transition: all 0.4s ease !important;
            width: 100%;
        }
        .stButton>button:hover {
            background: #ffd700 !important;
            color: #000 !important;
            box-shadow: 0 0 15px #ffd700, 0 0 30px rgba(255, 215, 0, 0.6) !important;
            transform: translateY(-2px);
        }

        /* Inputs Estilizados */
        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #fff !important;
            border: 1px solid rgba(255, 215, 0, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)
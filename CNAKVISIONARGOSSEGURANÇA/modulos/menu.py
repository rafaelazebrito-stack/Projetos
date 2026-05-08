import streamlit as st

def menu_principal():

    st.sidebar.title("MENU")

    opcao = st.sidebar.radio(
        "Escolha",
        [
            "Início"
        ]
    )

    st.title("Sistema CNAK Vision")
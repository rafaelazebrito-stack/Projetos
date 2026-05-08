import streamlit as st

from modulos.cadastro import tela_cadastro
from modulos.analytics import tela_analytics

def menu_principal():

    menu = st.sidebar.radio(
        "MENU",
        [
            "Cadastro",
            "Analytics"
        ]
    )

    if menu == "Cadastro":
        tela_cadastro()

    if menu == "Analytics":
        tela_analytics()

    if st.sidebar.button("Sair"):

        st.session_state.logado = False

        st.rerun()
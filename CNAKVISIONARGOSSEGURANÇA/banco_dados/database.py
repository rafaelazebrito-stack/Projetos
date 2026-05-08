import pandas as pd
import os
import streamlit as st
import time
from utilitarios.formatadores import Utils

class DatabaseHandler:
    def __init__(self, db_file, colunas):
        self.db_file = db_file
        self.colunas = colunas
        self._load_db()
    
    def _load_db(self):
        if 'db' not in st.session_state:
            if not os.path.exists(self.db_file):
                os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
                pd.DataFrame(columns=self.colunas).to_csv(self.db_file, index=False)
            df = pd.read_csv(self.db_file)
            for col in self.colunas:
                if col not in df.columns:
                    df[col] = 'N/A'
            st.session_state.db = df
            if st.session_state.db.empty and not st.session_state.get('seeded_random_users', False):
                self.seed_random_users(10)
                
    def get_all_users(self):
        return st.session_state.db
    
    def save_user(self, user_data):
        novo = pd.DataFrame([user_data], columns=self.colunas)
        st.session_state.db = pd.concat([st.session_state.db, novo], ignore_index=True)
        self._persist_db()
        return True
    
    def delete_users(self, documents_list):
        st.session_state.db = st.session_state.db[~st.session_state.db['Documento'].isin(documents_list)]
        self._persist_db()
    
    def _persist_db(self):
        st.session_state.db.to_csv(self.db_file, index=False)
    
    def is_duplicate(self, nome, document, email):
        df = st.session_state.db.copy()
        target_doc = document.replace('.', '').replace('-', '')
        db_docs = df['Documento'].astype(str).str.replace('.', '', regex=False).str.replace('-', '', regex=False)
        if target_doc in db_docs.values: return 'CPF'
        if nome.lower() in df['Nome'].astype(str).str.lower().values: return 'Nome'
        if email and email.lower() != 'n/a' and email.lower() in df['Email'].astype(str).str.lower().values: return 'Email'
        return None
    
    def seed_random_users(self, count=10):
        usuarios = []
        base = int(time.time())
        for i in range(count):
            usuario = Utils.gerar_usuario_ficticio(base + i, self.colunas)
            usuarios.append(usuario)
        if usuarios:
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame(usuarios)], ignore_index=True)
            self._persist_db()
            st.session_state.seeded_random_users = True
        return len(usuarios)
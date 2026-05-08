import json
import os

def carregar_logins(file_path):
    """
    Carrega os usuários garantindo que o tradutor (UTF-8) seja usado.
    """
    if not os.path.exists(file_path):
        return {}
    
    # FORÇANDO O ENCODING UTF-8 (ESSA É A CHAVE)
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        try:
            return json.load(f)
        except Exception as e:
            print(f"Erro ao ler JSON: {e}")
            return {}

def salvar_login(auth_data, file_path):
    """
    Salva os usuários garantindo que emojis e acentos não quebrem.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(auth_data, f, indent=4, ensure_ascii=False)
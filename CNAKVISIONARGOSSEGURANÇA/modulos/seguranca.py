import streamlit as st
import os
from datetime import datetime

def registrar_log(mensagem, relatorios_dir):
    """
    Função Motor de Auditoria: Grava ações em um arquivo .txt
    """
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_entry = f"[{data_hora}] - {mensagem}\n"
    
    caminho_log = os.path.join(relatorios_dir, "auditoria_sistema.txt")
    
    with open(caminho_log, "a", encoding="utf-8") as f:
        f.write(log_entry)

def exibir_monitoramento(db_handler, relatorios_dir):
    # (Mantém o código dos vídeos de estacionamento e shopping que já fizemos)
    st.markdown('<h2 class="glow-text">🎥 Central de Monitoramento Argos</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.video('https://assets.mixkit.co/videos/download/mixkit-car-parking-lot-night-action-1305.mp4')
    with col2:
        st.video('https://assets.mixkit.co/videos/download/mixkit-people-walking-in-shopping-mall-1110.mp4')

def exibir_auditoria(relatorios_dir):
    """
    Módulo: Auditoria & Logs (Item 1 solicitado)
    """
    st.markdown('<h2 class="glow-text">📋 Auditoria & Logs</h2>', unsafe_allow_html=True)
    
    caminho_log = os.path.join(relatorios_dir, "auditoria_sistema.txt")
    
    if os.path.exists(caminho_log):
        with open(caminho_log, "r", encoding="utf-8") as f:
            conteudo = f.readlines()
        
        # Exibe os últimos 20 logs de forma elegante
        st.markdown("### Histórico Recente de Ações")
        for log in reversed(conteudo[-20:]):
            st.code(log.strip(), language="bash")
            
        # Botão para baixar o relatório completo
        st.markdown("---")
        if st.button("GERAR RELATÓRIO PDF/TXT"):
            st.download_button(
                label="📥 Baixar Log Completo",
                data="".join(conteudo),
                file_name=f"auditoria_argos_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            registrar_log(f"Operador exportou o relatório de auditoria.", relatorios_dir)
    else:
        st.info("Nenhum registro de auditoria encontrado ainda.")
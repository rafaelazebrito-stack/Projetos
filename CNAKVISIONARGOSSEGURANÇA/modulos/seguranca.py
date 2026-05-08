import streamlit as st
import os
import pandas as pd
from datetime import datetime

# ==============================================================================
# 1. FUNÇÃO DE LOG (ESSENCIAL PARA TODOS OS MÓDULOS)
# ==============================================================================
def registrar_log(mensagem, diretorio_logs):
    """Garante a rastreabilidade industrial de todas as ações no sistema."""
    arquivo_log = os.path.join(diretorio_logs, "log_auditoria.txt")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Cria o diretório se não existir para evitar erros de escrita
    os.makedirs(diretorio_logs, exist_ok=True)
    
    with open(arquivo_log, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {mensagem}\n")

# ==============================================================================
# 2. FUNÇÃO: MONITORAMENTO DE VÍDEO (RESTAURADA E MELHORADA)
# ==============================================================================
def exibir_monitoramento(db_handler, diretorio_logs):
    """Interface Tática de Vigilância e Monitoramento."""
    st.markdown('<h2 class="glow-text">🎥 Monitoramento Vídeo // CNAK VISION</h2>', unsafe_allow_html=True)
    
    # Layout de Grade Industrial
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div style="border:1px solid #FFD700; padding:10px; background:#000;">', unsafe_allow_html=True)
        st.write("📡 **FEED DE VÍDEO PRINCIPAL - TERMINAL ATIVO**")
        # Simulação de placeholder de vídeo/camera
        st.image("https://img.freepik.com/premium-photo/cctv-camera-security-system-operating-with-digital-interface-screen_31965-15105.jpg", 
                 caption="STREAMING_ID: 085-CNAK-PROT", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("### 📊 Status de Rede")
        st.metric("Sinal LPR", "98%", delta="Excelente")
        st.metric("Frames/sec", "60 FPS", delta="Estável")
        st.metric("Latência", "12ms", delta="-2ms", delta_color="normal")
        
        if st.button("REINICIAR SERVIDOR DE VÍDEO", use_container_width=True):
            registrar_log("COMANDO: Reinício forçado do servidor de vídeo solicitado.", diretorio_logs)
            st.warning("Reiniciando protocolos de captura...")

# ==============================================================================
# 3. FUNÇÃO: AUDITORIA & LOGS (DESIGN INDUSTRIAL)
# ==============================================================================
def exibir_auditoria(diretorio_logs):
    """Painel de Compliance e Rastreabilidade Analítica."""
    st.markdown('<h2 class="glow-text">📋 Auditoria & Logs</h2>', unsafe_allow_html=True)
    
    arquivo_log = os.path.join(diretorio_logs, "log_auditoria.txt")

    if not os.path.exists(arquivo_log):
        st.info("Aguardando inicialização de registros...")
        return

    try:
        with open(arquivo_log, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        dados_log = []
        for linha in reversed(linhas):
            if " - " in linha:
                dt_hr, msg = linha.split(" - ", 1)
                
                # Inteligência de Categorização
                if "LOGIN" in msg: nivel, tag = "INFO", "🔵"
                elif "ERRO" in msg or "NEGADO" in msg: nivel, tag = "CRÍTICO", "🔴"
                elif "CADASTRO" in msg: nivel, tag = "OPERACIONAL", "🟡"
                else: nivel, tag = "SISTEMA", "⚪"

                dados_log.append({
                    "🕒 Timestamp": dt_hr,
                    "🛡️ Nível": f"{tag} {nivel}",
                    "📝 Evento": msg.strip()
                })

        df = pd.DataFrame(dados_log)

        # Dashboard de Auditoria
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "🕒 Timestamp": st.column_config.TextColumn(width="medium"),
                "🛡️ Nível": st.column_config.TextColumn(width="small"),
                "📝 Evento": st.column_config.TextColumn(width="large")
            }
        )

        st.download_button(
            "📊 EXPORTAR LOGS PARA COMPLIANCE",
            df.to_csv(index=False).encode('utf-8'),
            f"auditoria_cnak_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Erro ao processar registros de segurança: {e}")
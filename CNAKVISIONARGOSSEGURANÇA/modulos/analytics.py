import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def exibir_bi(db_handler):
    st.markdown('<div class="titulo-neon" style="font-size: 25px;">📊 BI & ANALYTICS</div>', unsafe_allow_html=True)
    df = db_handler.get_all_users()

    # Gráfico de Fluxo Animado (Simulado do original)
    st.markdown("#### 📈 Tendência de Fluxo Diário")
    datas = [f"Dia {i}" for i in range(1, 31)]
    fluxo = np.random.randint(3500, 6500, size=30)
    fig = go.Figure(data=go.Scatter(x=datas, y=fluxo, mode='lines+markers', line=dict(color='#ffd700')))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # Mapa de Calor
    st.markdown("#### 🌡️ Mapa de Calor de Densidade")
    z_data = np.random.randint(20, 100, size=(4, 3))
    fig_h = go.Figure(data=go.Heatmap(z=z_data, x=['Piso 1', 'Piso 2', 'Piso 3'], y=['Entrada', 'Praça', 'Lojas', 'Estac.'], colorscale='YlOrBr'))
    fig_h.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig_h, use_container_width=True)
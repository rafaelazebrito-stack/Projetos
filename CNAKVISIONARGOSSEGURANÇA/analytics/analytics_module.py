import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

def gerar_dados_simulados_bi():
    np.random.seed(42)
    datas = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
    fluxo_diario = np.random.randint(3500, 6500, size=30).tolist()
    tipos = ['Diretoria', 'Operacional', 'Lojista', 'Visitante']
    dados_tipo = {tipo: np.random.randint(100, 800, size=30).tolist() for tipo in tipos}
    andares = ['Piso 1', 'Piso 2', 'Piso 3']
    dados_andar = {andar: np.random.randint(800, 2000, size=30).tolist() for andar in andares}
    return {'datas': datas, 'fluxo_diario': fluxo_diario, 'dados_tipo': dados_tipo, 'dados_andar': dados_andar}

def exibir_bi(db_handler):
    st.markdown('<div class="dashboard-card"><h3 class="glow-text">📊 Painel de Business Intelligence</h3></div>', unsafe_allow_html=True)
    dados = gerar_dados_simulados_bi()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Prédios", "4")
    c2.metric("Andares", "3")
    c3.metric("Lojas", "50")
    c4.metric("Fluxo Total", "5.000")

    # Gráfico Animado
    fig = go.Figure()
    cores = {'Diretoria': '#ffd700', 'Operacional': '#b8860b', 'Lojista': '#daa520', 'Visitante': '#ffa500'}
    for tipo, valores in dados['dados_tipo'].items():
        fig.add_trace(go.Scatter(x=dados['datas'], y=valores, mode='lines+markers', name=tipo, line=dict(color=cores.get(tipo, '#ffd700'))))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', title="Fluxo por Tipo de Acesso")
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de Andares
    fig_bar = go.Figure()
    for andar, valores in dados['dados_andar'].items():
        fig_bar.add_trace(go.Bar(name=andar, x=dados['datas'][-7:], y=valores[-7:]))
    fig_bar.update_layout(template='plotly_dark', barmode='group', title="Fluxo por Andar (Últimos 7 dias)")
    st.plotly_chart(fig_bar, use_container_width=True)
import streamlit as st

def exibir_marketplace():
    st.markdown('<div class="titulo-neon" style="font-size: 25px;">💎 MARKETPLACE DE DADOS</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **ESSENTIAL BI**")
        st.write("R$ 200,00/mês")
        if st.button("ASSINAR ESSENTIAL"): st.success("Contratado!")
    with col2:
        st.success("🔥 **HEATMAP PRO**")
        st.write("R$ 650,00/mês")
        if st.button("ASSINAR HEATMAP"): st.success("Contratado!")
    with col3:
        st.warning("🚀 **VISION AI**")
        st.write("R$ 1.000,00/mês")
        if st.button("ASSINAR VISION AI"): st.success("Contratado!")
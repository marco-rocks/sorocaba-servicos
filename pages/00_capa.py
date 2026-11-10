import streamlit as st

st.set_page_config(
    page_title="Capa — Mercado do Trabalho e Serviços em Sorocaba",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
.hero {
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
  color: #fff;
  border-radius: 20px;
  padding: 4.5rem 2rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
  margin-bottom: 2rem;
}
.hero h1 {
  font-size: 2.7rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  color: #ffffff;
  letter-spacing: -0.5px;
  line-height: 1.2;
}
.hero h3 {
  font-weight: 300;
  margin: 0 0 2rem 0;
  color: #cfe3ea;
  font-size: 1.35rem;
}
.hero p {
  margin: 0.35rem 0;
  font-size: 1.1rem;
  color: #e6f1f5;
}
.hero .meta {
  margin-top: 2rem;
  font-weight: 600;
  color: #90caf9;
  letter-spacing: 1px;
}
</style>

<div class="hero">
  <h1>MERCADO DO TRABALHO EM SOROCABA E EXPLANAÇÃO SOBRE O SETOR DE SERVIÇOS</h1>
  <h3>Panorama Estrutural, Empreendedorismo e Dinâmica do Mercado de Trabalho e do Setor Terciário</h3>
  <p><b>Análise Econômica Aplicada e Ciência de Dados</b></p>
  <p>Região Metropolitana de Sorocaba (RMS) · Estado de São Paulo</p>
  <p class="meta">SOROCABA - SP · 2026</p>
</div>
""", unsafe_allow_html=True)

st.write("")

c1, c2, c3 = st.columns([1, 1, 2])
c1.page_link("pages/00_sumario.py", label="Acessar Sumário", icon="📑")
c2.page_link("pages/00_equipe.py", label="Conhecer a Equipe", icon="👥")

st.markdown("---")

st.subheader("🎯 Sobre o Projeto")
st.markdown("""
Este projeto apresenta uma investigação analítica e exploratória orientada por dados sobre o comportamento do **Setor de Serviços** e do **Mercado de Trabalho Formal** em Sorocaba (SP).

Por meio da integração de microdados oficiais do **IBGE (Censos Demográficos e CEMPRE)**, do **Ministério do Trabalho e Emprego (RAIS e CAGED)** e da **Receita Federal / Sebrae-SP**, o dashboard permite compreender a distribuição espacial, a evolução histórica do MEI, a composição da massa salarial e os fluxos de mobilidade regional na sede metropolitana.
""")

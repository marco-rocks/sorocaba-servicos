import streamlit as st

# Configuração global da página
st.set_page_config(
    page_title="MERCADO DO TRABALHO EM SOROCABA E EXPLANAÇÃO SOBRE O SETOR DE SERVIÇOS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DEFINIÇÃO DAS PÁGINAS ATIVAS ---
p_capa = st.Page("pages/00_capa.py", title="Capa do Projeto", icon="🏠", default=True)
p_sumario = st.Page("pages/00_sumario.py", title="Sumário da Apresentação", icon="📑")
p_equipe = st.Page("pages/00_equipe.py", title="Equipe & Integrantes", icon="👥")
p_etl = st.Page("pages/07_metodologia_etl.py", title="Metodologia ETL", icon="⚙️")
p_panorama = st.Page("pages/00_panorama.py", title="Panorama & Histórico", icon="🏛️")
p_contexto = st.Page("pages/01_contexto.py", title="01 — Contexto Econômico & PIB", icon="🏙️")
p_mercado = st.Page("pages/02_mercado_trabalho.py", title="02 — Mercado de Trabalho", icon="💼")
p_servicos = st.Page("pages/03_setor_servicos.py", title="03 — Setor de Serviços", icon="🛎️")
p_salario_ocupacao = st.Page("pages/04_salario_ocupacao.py", title="04 — Salário & Ocupações", icon="💰")
p_mobilidade = st.Page("pages/05_mobilidade.py", title="05 — Mobilidade Urbana", icon="🚗")
p_conclusao = st.Page("pages/06_conclusao.py", title="06 — Conclusão & Diretrizes", icon="🎯")

# Navegação na barra lateral
pg = st.navigation({
    "📌 Apresentação & Contexto": [
        p_capa,
        p_sumario,
        p_equipe,
        p_etl,
        p_panorama
    ],
    "📊 Diagnóstico Socioeconômico": [
        p_contexto,
        p_mercado,
        p_servicos,
        p_salario_ocupacao,
        p_mobilidade,
        p_conclusao
    ]
})

pg.run()

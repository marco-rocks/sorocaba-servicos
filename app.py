import streamlit as st

# Configuração global da página
st.set_page_config(
    page_title="Mercado de Trabalho e Empreendedorismo Sorocabano: O papel dos serviços e a mobilidade laboral intermunicipal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DEFINIÇÃO DAS PÁGINAS ATIVAS ---
p_capa = st.Page("pages/00_capa.py", title="Capa Institucional", icon="🏠", default=True)
p_sumario = st.Page("pages/00_sumario.py", title="Sumário Executivo", icon="📑")
p_equipe = st.Page("pages/00_equipe.py", title="Corpo Técnico & Pesquisadores", icon="👥")
p_etl = st.Page("pages/07_metodologia_etl.py", title="Metodologia & Engenharia de Dados", icon="⚙️")
p_panorama = st.Page("pages/00_panorama.py", title="Panorama Histórico de Sorocaba", icon="🏛️")
p_contexto = st.Page("pages/01_contexto.py", title="01 — Contexto Macroeconômico e Demografia", icon="🏙️")
p_mercado = st.Page("pages/02_mercado_trabalho.py", title="02 — Dinâmica do Emprego Formal e Empresas", icon="💼")
p_salario_ocupacao = st.Page("pages/04_salario_ocupacao.py", title="03 — Estrutura Ocupacional, Salários e TGCA", icon="💰")
p_mobilidade = st.Page("pages/05_mobilidade.py", title="04 — Mobilidade Pendular e Integração Regional", icon="🚗")
p_servicos = st.Page("pages/03_setor_servicos.py", title="05 — Setor de Serviços e Empreendedorismo (MEI)", icon="🛎️")
p_conclusao = st.Page("pages/06_conclusao.py", title="06 — Síntese Estratégica e Diretrizes de Políticas Públicas", icon="🎯")

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
        p_salario_ocupacao,
        p_mobilidade,
        p_servicos,
        p_conclusao
    ]
})

pg.run()

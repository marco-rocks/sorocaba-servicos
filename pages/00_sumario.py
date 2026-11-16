import streamlit as st

st.set_page_config(
    page_title="Sumário Executivo",
    page_icon="📑",
    layout="wide"
)

st.title("📑 Sumário Executivo do Projeto")
st.markdown("Navegue diretamente pelos módulos da pesquisa através dos atalhos abaixo:")
st.write("")

TOPICOS = [
    {
        "titulo": "Capa Institucional",
        "icone": "🏠",
        "arquivo": "pages/00_capa.py",
        "descricao": "Apresentação institucional, título oficial e contextualização do projeto."
    },
    {
        "titulo": "Corpo Técnico & Pesquisadores",
        "icone": "👥",
        "arquivo": "pages/00_equipe.py",
        "descricao": "Identificação dos integrantes, pesquisadores e responsáveis pelo desenvolvimento."
    },
    {
        "titulo": "Metodologia & Engenharia de Dados",
        "icone": "⚙️",
        "arquivo": "pages/07_metodologia_etl.py",
        "descricao": "Arquitetura do pipeline de dados: extração de dados públicos (IBGE/RAIS/Sebrae), transformação (limpeza, IPCA, TGCA) e carga otimizada."
    },
    {
        "titulo": "Panorama Histórico de Sorocaba",
        "icone": "🏛️",
        "arquivo": "pages/00_panorama.py",
        "descricao": "Indicadores macroeconômicos chave, evolução histórica econômica (Bandeirantismo à Manchester Paulista) e órgãos institucionais de apoio ao trabalho e empreendedorismo."
    },
    {
        "titulo": "01 — Contexto Macroeconômico e Demografia",
        "icone": "🏙️",
        "arquivo": "pages/01_contexto.py",
        "descricao": "Evolução do PIB Real (Preços constantes em 2023), transição demográfica e ênfase nas taxas percentuais por faixa de idade (Censo 2010 vs 2022)."
    },
    {
        "titulo": "02 — Dinâmica do Emprego Formal e Empresas",
        "icone": "💼",
        "arquivo": "pages/02_mercado_trabalho.py",
        "descricao": "Evolução de empresas e empregos formais (CEMPRE), remuneração em salários mínimos e comparação regional com municípios do Estado (Itu, Salto e Araçoiaba)."
    },
    {
        "titulo": "03 — Estrutura Ocupacional, Salários e TGCA",
        "icone": "💰",
        "arquivo": "pages/04_salario_ocupacao.py",
        "descricao": "Microdados da RAIS/CBO, ranking de vínculos e massa salarial, e cálculo da Taxa Geométrica de Crescimento Anual (TGCA) das profissões."
    },
    {
        "titulo": "04 — Mobilidade Pendular e Integração Regional",
        "icone": "🚗",
        "arquivo": "pages/05_mobilidade.py",
        "descricao": "Deslocamentos pendulares para trabalho, taxa de mobilidade intermunicipal e retenção da mão de obra na Região Metropolitana."
    },
    {
        "titulo": "05 — Setor de Serviços e Empreendedorismo (MEI)",
        "icone": "🛎️",
        "arquivo": "pages/03_setor_servicos.py",
        "descricao": "O que integra o setor de serviços (CNAE 2.0), subsetores, evolução do MEI acumulado, distinção entre MEIs ativos e inativos e mapa territorial da cidade."
    },
    {
        "titulo": "06 — Síntese Estratégica e Diretrizes de Políticas Públicas",
        "icone": "🎯",
        "arquivo": "pages/06_conclusao.py",
        "descricao": "Síntese dos resultados, desafios de produtividade e recomendações de políticas públicas e qualificação para Sorocaba."
    }
]

for t in TOPICOS:
    label_text = t["titulo"]
    with st.container():
        c1, c2 = st.columns([1.2, 3])
        c1.page_link(t["arquivo"], label=label_text, icon=t["icone"])
        c2.caption(t["descricao"])
        st.markdown("<hr style='margin: 0.4rem 0;'>", unsafe_allow_html=True)

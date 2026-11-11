import base64
import mimetypes
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Equipe do Projeto",
    page_icon="👥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"

st.title("👥 Integrantes do Projeto")
st.markdown("Equipe responsável pela pesquisa, tratamento de bases de dados, modelagem analítica e desenvolvimento do dashboard.")
st.write("")

# Lista de integrantes do projeto
EQUIPE = [
    {
        "nome": "Marco Túlio",
        "funcao": "Desenvolvimento & Análise de Dados",
        "foto": "marco.png",
        "bio": "Engenharia de dados, integração de microdados oficiais, versionamento do projeot e estruturação do painel interativo Streamlit."
    },
    {
        "nome": "Fábio França",
        "funcao": "Pesquisa Econômica & Modelagem",
        "foto": "fabio.jpg",
        "bio": "Pesquisa setorial sobre o ecossistema de serviços, indicadores macroeconômicos e validação analítica."
    },
    {
        "nome": "Matheus Bueno",
        "funcao": "Pesquisa População & PIB",
        "foto": "matheus.jpg",
        "bio": "Pesquisa sobre o PIB da cidade de Sorocaba, distribuição da população e análise do contexto econômico."
    },
    {
        "nome": "Gabriel Castilho ",
        "funcao": "Pesquisa & Estrutura do Mercado ",
        "foto": "gabriel.jpeg",
        "bio": "Pesquisa acerca da organização do mercado de trabalho, análise de salários, regiões e crescimento empresarial"
    },
    {
        "nome": "Flávia Sartori",
        "funcao": "Pesquisa & Mobilidade Urbana",
        "foto": "flavia.png",
        "bio": "Análise demográfica censitária, levantamento territorial dos polos comerciais e dinâmica da mobilidade regional."
    },
    {
        "nome": "Luiz Machado",
        "funcao": "Pesquisa & Salário/Ocupações",
        "foto": "luiz.jpg",
        "bio": "Análise ocupacional, distribuição salarial e crescimento do mercado de trabalho e do setor de serviços"
    },
]

def carregar_avatar(foto_nome: str, nome: str) -> str:
    """Carrega a imagem real da pasta assets em base64 ou gera um avatar vetorial com as iniciais."""
    if foto_nome:
        caminho = ASSETS_DIR / foto_nome
        if caminho.exists():
            mime = mimetypes.guess_type(caminho.name)[0] or "image/jpeg"
            b64 = base64.b64encode(caminho.read_bytes()).decode("utf-8")
            return f"data:{mime};base64,{b64}"
    
    iniciais = "".join(p[0] for p in nome.split()[:2]).upper() or "?"
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180">'
        '<rect width="180" height="180" fill="#203a43"/>'
        '<text x="50%" y="50%" fill="#ffffff" font-size="60" font-family="Arial, sans-serif" '
        f'text-anchor="middle" dominant-baseline="central">{iniciais}</text></svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("utf-8")

st.markdown("""
<style>
.card-membro {
  background: #f8f9fa;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.8rem 1rem;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-bottom: 1.5rem;
  height: 100%;
}
.card-membro:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.card-membro img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid #203a43;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  margin-bottom: 1rem;
}
.card-membro .nome {
  font-weight: 700;
  font-size: 1.2rem;
  color: #1e293b;
  margin-bottom: 0.3rem;
}
.card-membro .funcao {
  font-weight: 600;
  font-size: 0.95rem;
  color: #0284c7;
  margin-bottom: 0.8rem;
}
.card-membro .bio {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(len(EQUIPE))

for col, m in zip(cols, EQUIPE):
    img_data = carregar_avatar(m.get("foto"), m["nome"])
    with col:
        st.markdown(f"""
        <div class="card-membro">
          <img src="{img_data}" alt="{m['nome']}">
          <div class="nome">{m['nome']}</div>
          <div class="funcao">{m['funcao']}</div>
          <div class="bio">{m.get('bio', '')}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
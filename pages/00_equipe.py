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
        "cargo": "Pesquisador (Fatec Votorantim)",
        "funcao": "Engenharia de Dados",
        "foto": "marco.png",
        "bio": "Pesquisa em análise quantitativa e inteligência de dados (mercado financeiro e criptoativos). Responsável pela arquitetura de dados, integração de microdados oficiais (RAIS/IBGE) e desenvolvimento do dashboard."
    },
    {
        "nome": "Fábio França",
        "cargo": "Estagiário de Análise de Dados (Frasle Mobility)",
        "funcao": "Modelagem Analítica & Econometria",
        "foto": "fabio.jpg",
        "bio": "Pesquisa setorial aplicada ao setor terciário, extração de indicadores macroeconômicos, tratamento de séries temporais e validação estatística."
    },
    {
        "nome": "Matheus Bueno",
        "cargo": "Estagiário de Custos e Manufatura (CNH Industrial)",
        "funcao": "Análise Demográfica & PIB Real",
        "foto": "matheus.jpg",
        "bio": "Estudo sobre a dinâmica do PIB municipal a preços constantes, transição etária nos Censos Demográficos e correlação entre estrutura produtiva e crescimento socioeconômico."
    },
    {
        "nome": "Gabriel Castilho",
        "cargo": "Auxiliar de TI (Edscha do Brasil)",
        "funcao": "Infraestrutura & Mercado de Trabalho",
        "foto": "gabriel.jpeg",
        "bio": "Apoio a ferramentas tecnológicas, processamento de vínculos empregatícios formais, mapeamento de densidade empresarial (CEMPRE) e dinâmica das empresas locais."
    },
    {
        "nome": "Flávia Sartori",
        "cargo": "Estagiária de Risco e Crédito (Afinz)",
        "funcao": "Pesquisa Regional & Mobilidade Laboral",
        "foto": "flavia.png",
        "bio": "Investigação censitária dos fluxos pendulares intermunicipais, taxas de mobilidade de mão de obra e polarização dos serviços na Região Metropolitana de Sorocaba."
    },
    {
        "nome": "Luiz Machado",
        "cargo": "Analista de Inteligência Comercial (Rodopiro)",
        "funcao": "Estrutura Salarial & Ocupações",
        "foto": "luiz.jpg",
        "bio": "Pesquisa ocupacional (CBO/RAIS), modelagem da massa de rendimentos, cálculo da Taxa Geométrica de Crescimento Anual (TGCA) e hierarquia de remuneração."
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
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  padding: 1.8rem 1.4rem;
  text-align: center;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  height: 100%;
}
.card-membro:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 28px rgba(0,0,0,0.1);
  border-color: #cbd5e1;
}
.card-membro img {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid #203a43;
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
  margin: 0 auto 1.1rem auto;
}
.card-membro .nome {
  font-weight: 700;
  font-size: 1.25rem;
  color: #0f172a;
  margin-bottom: 0.35rem;
}
.card-membro .cargo {
  display: inline-block;
  background: #e0f2fe;
  color: #0369a1;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 0.25rem 0.65rem;
  border-radius: 8px;
  margin: 0 auto 0.5rem auto;
}
.card-membro .funcao {
  font-weight: 600;
  font-size: 0.95rem;
  color: #0f766e;
  margin-bottom: 0.85rem;
}
.card-membro .bio {
  font-size: 0.88rem;
  color: #475569;
  line-height: 1.55;
  text-align: left;
}
</style>
""", unsafe_allow_html=True)

# Grid em 2 linhas x 3 colunas para garantir leitura ampla e cards confortáveis
for i in range(0, len(EQUIPE), 3):
    bloco = EQUIPE[i:i+3]
    cols = st.columns(3)
    for col, m in zip(cols, bloco):
        img_data = carregar_avatar(m.get("foto"), m["nome"])
        with col:
            st.markdown(f"""
            <div class="card-membro">
              <img src="{img_data}" alt="{m['nome']}">
              <div class="nome">{m['nome']}</div>
              <div class="cargo">{m.get('cargo', '')}</div>
              <div class="funcao">{m['funcao']}</div>
              <div class="bio">{m.get('bio', '')}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
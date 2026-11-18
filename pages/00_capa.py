import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Capa — Mercado de Trabalho e Empreendedorismo Sorocabano",
    page_icon="🏠",
    layout="wide"
)

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
qr_path = ASSETS_DIR / "qrcode_app.png"
with open(qr_path, "rb") as f:
    qr_b64 = base64.b64encode(f.read()).decode("utf-8")

st.markdown(f"""
<style>
.hero {{
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
  color: #fff;
  border-radius: 20px;
  padding: 3.5rem 2.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
  margin-bottom: 2rem;
}}
.hero-container {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
}}
.hero-text {{
  flex: 1 1 560px;
  text-align: left;
}}
.hero h1 {{
  font-size: 2.35rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  color: #ffffff;
  letter-spacing: -0.5px;
  line-height: 1.25;
}}
.hero h3 {{
  font-weight: 300;
  margin: 0 0 1.5rem 0;
  color: #cfe3ea;
  font-size: 1.2rem;
  line-height: 1.4;
}}
.hero p {{
  margin: 0.35rem 0;
  font-size: 1.05rem;
  color: #e6f1f5;
}}
.hero .meta {{
  margin-top: 1.5rem;
  font-weight: 600;
  color: #90caf9;
  letter-spacing: 1px;
  font-size: 0.95rem;
}}
.hero .badge-temporal {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  padding: 0.35rem 0.9rem;
  margin-top: 1.2rem;
  font-size: 0.88rem;
  color: #f0fdf4;
  font-weight: 600;
  letter-spacing: 0.5px;
}}
.qr-card {{
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
  text-align: center;
  max-width: 210px;
  margin: 0 auto;
}}
.qr-card img {{
  width: 170px;
  height: 170px;
  border-radius: 8px;
}}
.qr-card .qr-label {{
  color: #0f2027;
  font-weight: 700;
  font-size: 0.85rem;
  margin-top: 0.6rem;
  margin-bottom: 0.2rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
.qr-card a {{
  color: #1976d2;
  font-size: 0.75rem;
  text-decoration: none;
  font-weight: 600;
  word-break: break-all;
}}
.qr-card a:hover {{
  text-decoration: underline;
}}
</style>

<div class="hero">
  <div class="hero-container">
    <div class="hero-text">
      <h1>Mercado de Trabalho e Empreendedorismo Sorocabano: O papel dos serviços e a mobilidade laboral intermunicipal</h1>
      <h3>Panorama Estrutural, Empreendedorismo e Dinâmica do Mercado de Trabalho e do Setor Terciário</h3>
      <p><b>Análise Econômica Aplicada e Ciência de Dados</b></p>
      <p>Região Metropolitana de Sorocaba (RMS) · Estado de São Paulo</p>
      <div class="badge-temporal">
        📅 <b>Série Temporal dos Dados:</b> 2002 – 2026
      </div>
      <p class="meta">SOROCABA - SP · 2026</p>
    </div>
    <div class="qr-card">
      <img src="data:image/png;base64,{qr_b64}" alt="QR Code do App" />
      <span class="qr-label">Acesse o Dashboard</span>
      <a href="https://trabalho-em-sorocaba.streamlit.app/" target="_blank">Link do Dashboard</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

c1, c2, c3 = st.columns([1, 1, 2])
c1.page_link("pages/00_sumario.py", label="Acessar Sumário Executivo", icon="📑")
c2.page_link("pages/00_equipe.py", label="Conhecer o Corpo Técnico", icon="👥")

st.markdown("---")

st.subheader("🎯 Sobre o Projeto")
st.markdown("""
Este projeto apresenta uma investigação analítica e exploratória orientada por dados sobre o comportamento do **Setor de Serviços** e do **Mercado de Trabalho Formal** em Sorocaba (SP).

Por meio da integração de microdados oficiais do **IBGE (Censos Demográficos e CEMPRE)**, do **Ministério do Trabalho e Emprego (RAIS e CAGED)** e da **Receita Federal / Sebrae-SP**, o dashboard permite compreender a distribuição espacial, a evolução histórica do MEI, a composição da massa salarial e os fluxos de mobilidade regional na sede metropolitana.

* **Janela Temporal Consolidada:** Registros históricos e contemporâneos compreendidos entre **2002 e 2026** (incluindo a série histórica do PIB Municipal a preços constantes de 2002 a 2023, evolução empresarial formal e MEI da Receita Federal/Sebrae, microdados da RAIS de 2019 a 2023 e dados censitários do IBGE).
""")

st.markdown("---")
st.subheader("📸 Sorocaba em Foco")
col_img1, col_img2 = st.columns(2)
with col_img1:
    img_rio = ASSETS_DIR / "sorocaba_ciclovia_rio.jpg"
    if img_rio.exists():
        st.image(str(img_rio), caption="Margens do Rio Sorocaba e malha cicloviária urbana integrada", use_container_width=True)

with col_img2:
    img_bot = ASSETS_DIR / "sorocaba_jardim_botanico.jpg"
    if img_bot.exists():
        st.image(str(img_bot), caption="Palacete de Cristal no Jardim Botânico Irmãos Villas-Bôas", use_container_width=True)

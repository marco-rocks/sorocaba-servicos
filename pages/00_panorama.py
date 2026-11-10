import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_CONTEXTO_DIR = BASE_DIR / "data" / "raw" / "contexto"

@st.cache_data
def carregar_metricas():
    metricas = {
        "populacao_val": "723.682 hab",
        "populacao_delta": "+23,36% vs 2010",
        "pib_label": "PIB Real (2023)",
        "pib_val": "R$ 58,82 Bi",
        "pib_delta": "+3,22% no ano",
        "empregos_val": "261.583",
        "empregos_delta": "RAIS / MTE",
        "salario_val": "R$ 4.099,96",
        "salario_sub": "Média Formal"
    }

    # 1. População
    file_pop = PROCESSED_DIR / "populacao_limpo.csv"
    if file_pop.exists():
        df_pop = pd.read_csv(file_pop)
        row_tot = df_pop[df_pop["Faixa Etária"] == "Total General"]
        if not row_tot.empty:
            tot_2022 = int(row_tot["População (2022)"].values[0])
            cresc_pct = float(row_tot["Crescimento (%)"].values[0])
            metricas["populacao_val"] = f"{tot_2022:,.0f}".replace(",", ".") + " hab"
            metricas["populacao_delta"] = f"+{cresc_pct:.2f}% vs 2010".replace(".", ",")

    # 2. PIB Real
    file_pib = PROCESSED_DIR / "pib_limpo.csv"
    if file_pib.exists():
        df_pib = pd.read_csv(file_pib).sort_values("Ano")
        if not df_pib.empty:
            ult = df_pib.iloc[-1]
            metricas["pib_label"] = f"PIB Real ({int(ult['Ano'])})"
            metricas["pib_val"] = f"R$ {ult['PIB Real 2023 (R$)']/1e9:.2f} Bi".replace(".", ",")
            if pd.notna(ult["Crescimento Real (%)"]):
                metricas["pib_delta"] = f"{ult['Crescimento Real (%)']:+.2f}% no ano".replace(".", ",")

    # 3. Empregos e Salários (Resumo)
    file_resumo = RAW_CONTEXTO_DIR / "trabalhadores_e_populacao_sorocaba.csv"
    if file_resumo.exists():
        try:
            df_res = pd.read_csv(file_resumo, sep=";", encoding="utf-8")
            row_rais = df_res[df_res["Indicador"].str.contains("Trabalhadores com Carteira", na=False)]
            row_sal = df_res[df_res["Indicador"].str.contains("Salário Médio", na=False)]
            row_caged = df_res[df_res["Indicador"].str.contains("Saldo Anual", na=False)]

            if not row_rais.empty:
                val_rais = int(float(row_rais["Valor"].values[0]))
                metricas["empregos_val"] = f"{val_rais:,.0f}".replace(",", ".")
            if not row_caged.empty:
                val_caged = int(float(row_caged["Valor"].values[0]))
                metricas["empregos_delta"] = f"+{val_caged:,.0f} saldo CAGED".replace(",", ".")
            if not row_sal.empty:
                val_sal = float(row_sal["Valor"].values[0])
                metricas["salario_val"] = f"R$ {val_sal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                metricas["salario_sub"] = "RAIS / MTE"
        except Exception:
            pass

    return metricas

st.title("MERCADO DO TRABALHO EM SOROCABA E EXPLANAÇÃO SOBRE O SETOR DE SERVIÇOS")
st.subheader("Panorama estrutural, dinâmica do emprego, renda e serviços na Região Metropolitana")
st.markdown("---")

m = carregar_metricas()
col1, col2, col3, col4 = st.columns(4)
col1.metric("População (Censo 2022)", m["populacao_val"], m["populacao_delta"])
col2.metric(m["pib_label"], m["pib_val"], m["pib_delta"])
col3.metric("Empregos Formais", m["empregos_val"], m["empregos_delta"])
col4.metric("Salário Médio Formal", m["salario_val"], m["salario_sub"])

# --- INFORMAÇÕES DE CONTEXTO ---
st.markdown("---")
st.header("🏙️ Panorama Histórico, Geográfico e Institucional de Sorocaba")

tab1, tab2, tab3 = st.tabs(["🏛️ Origem & Indicadores", "⏳ Linha do Tempo Histórica", "🏢 Gestão & Apoio ao Trabalhador e Empreendedor"])

with tab1:
    st.subheader("Origem, Fundação e Posição Regional")
    st.markdown("""
    * **Origem e Fundação:** Povoada originalmente pelos índios Tupiniquins e cortada pelo histórico Caminho do Peabiru, a região era rota para bandeirantes e missionários. Fundada oficialmente em 1654 pelo capitão bandeirante Baltazar Fernandes, seu nome vem do Tupi-Guarani ("terra rasgada"). Em 1661, tornou-se Vila com 30 famílias.
    * **Relevância Econômica:** Sede da Região Metropolitana de Sorocaba (RMS) composta por 27 municípios e mais de 2,1 milhões de habitantes, atuando como polo concentrador de comércio, saúde, tecnologia e serviços especializados.
    * **Localização Estratégica:** A 87 km da capital paulista, servida pelos eixos rodoviários Castello Branco e Raposo Tavares. Abriga o Parque Tecnológico de Sorocaba (PTS), indústrias automotivas, aeronáuticas e um ecossistema pujante de startups e logística.
    """)

with tab2:
    st.subheader("Evolução Histórica da Economia Sorocabana")
    st.markdown("""
    * **Séc. XVII (Anos 1600) — Ciclo do Bandeirantismo:** Ponto de partida para expedições ao interior do Brasil e expansão das fronteiras nacionais.
    * **Séc. XVIII e XIX (1733-1890) — Ciclo do Tropeirismo:** Em 1733 ocorreu a passagem da primeira tropa de muares, tornando Sorocaba a capital das Feiras de Muares e conectando os mercados do Sul ao Sudeste e Nordeste do país.
    * **1818 — Pioneirismo Siderúrgico:** Inauguração dos altos-fornos da Real Fábrica de Ferro São João do Ipanema, marco fundacional da metalurgia na América Latina.
    * **1856 — Ciclo do Algodão:** Introdução do cultivo do algodão herbáceo impulsionado pela demanda de exportação para a Europa no contexto da Guerra Civil Americana.
    * **1875 — Conexão Férrea:** Inauguração da Estrada de Ferro Sorocabana (EFS) por iniciativa do empresário Luiz Matheus Maylasky para escoar a produção regional.
    * **Fim do Séc. XIX e Séc. XX — A "Manchester Paulista":** Instalação de grandes complexos têxteis (Nossa Senhora da Ponte, Santa Rosália e Votorantim), consolidando a cidade como um polo operário e industrial de primeira grandeza.
    """)

with tab3:
    st.subheader("Gestão de Emprego, Qualificação, Empreendedorismo e Desenvolvimento")
    st.markdown("""
    * **Secretaria do Empreendedorismo / SEDET (Secretaria de Desenvolvimento Econômico e Turismo):**
        * Articula políticas públicas voltadas ao ambiente de negócios, fomento à inovação, atração de investimentos privados e estímulo ao micro e pequeno empreendedor.
        * Coordena a desburocratização da abertura e regularização de empresas e MEIs através do **Espaço Empreendedor / Banco do Povo Paulista**.
        * Integra iniciativas junto ao Parque Tecnológico de Sorocaba (PTS), Sebrae-SP, associações comerciais (ACSO) e sindicatos patronais do setor de serviços.
    * **SERTE (Secretaria de Relações do Trabalho e Qualificação Profissional):**
        * **Uniten (Universidade do Trabalhador Empreendedor e Negócios):** Oferece programas contínuos e gratuitos de capacitação profissional e formação empreendedora.
        * **Casa do Trabalhador (SINE Municipal / PAT):** Centralizada no Centro (Rua Cel. Cavalheiros, 353), atua no encaminhamento a vagas, emissão de CTPS digital e seguro-desemprego.
        * **Van do Emprego e Qualificação:** Unidade móvel que descentraliza cadastros e processos seletivos pelas diferentes zonas e feiras da cidade.
    """)

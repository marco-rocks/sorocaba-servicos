import streamlit as st
import pandas as pd
from pathlib import Path

# Configuração global da página
st.set_page_config(
    page_title="Setor de Serviços - Sorocaba",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_CONTEXTO_DIR = BASE_DIR / "data" / "raw" / "contexto"

@st.cache_data
def carregar_metricas():
    metricas = {
        "populacao_val": "723.682 hab",
        "populacao_delta": "+23.36% vs 2010",
        "pib_label": "PIB Real (2023)",
        "pib_val": "R$ 58.82 Bi",
        "pib_delta": "+3.22% no ano",
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
            metricas["populacao_delta"] = f"+{cresc_pct:.2f}% vs 2010"

    # 2. PIB Real
    file_pib = PROCESSED_DIR / "pib_limpo.csv"
    if file_pib.exists():
        df_pib = pd.read_csv(file_pib).sort_values("Ano")
        if not df_pib.empty:
            ult = df_pib.iloc[-1]
            metricas["pib_label"] = f"PIB Real ({int(ult['Ano'])})"
            metricas["pib_val"] = f"R$ {ult['PIB Real 2023 (R$)']/1e9:.2f} Bi"
            if pd.notna(ult["Crescimento Real (%)"]):
                metricas["pib_delta"] = f"{ult['Crescimento Real (%)']:+.2f}% no ano"

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

# --- FUNÇÃO DA PÁGINA INICIAL ---
def renderizar_home():
    st.title("📊 Análise Econômica: O Setor de Serviços em Sorocaba-SP")
    st.subheader("Como o setor de serviços influencia o mercado de trabalho local?")

    st.markdown("""
    ---
    ### 🎯 Objetivo do Projeto
    Esta aplicação analisa a estrutura econômica do município de **Sorocaba (SP)**, com foco especial na relevância e no impacto do **Setor de Serviços** sobre a geração de empregos, massa salarial e dinâmica regional.

    #### 🧭 Estrutura da Narrativa
    Navegue pelo menu lateral à esquerda para navegar pelas seções.
    ---
    """)

    m = carregar_metricas()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("População (Censo 2022)", m["populacao_val"], m["populacao_delta"])
    col2.metric(m["pib_label"], m["pib_val"], m["pib_delta"])
    col3.metric("Empregos Formais", m["empregos_val"], m["empregos_delta"])
    col4.metric("Salário Médio Formal", m["salario_val"], m["salario_sub"])

# --- DEFINIÇÃO DAS PÁGINAS ACTIVAS ---
p_home = st.Page(renderizar_home, title="Página Inicial", icon="🏠", default=True)
p_contexto = st.Page("pages/01_contexto.py", title="01 — Contexto Econômico", icon="🏙️")
p_mercado = st.Page("pages/02_mercado_trabalho.py", title="02 — Mercado de Trabalho", icon="💼")

# Navegação na barra lateral
pg = st.navigation({
    "📊 Serviços em Sorocaba": [
        p_home,
        p_contexto,
        p_mercado,
    ]
})

pg.run()
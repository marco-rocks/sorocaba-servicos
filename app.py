import streamlit as st
import pandas as pd
from pathlib import Path

# 1. Configuração global da página
st.set_page_config(
    page_title="Setor de Serviços - Sorocaba",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminhos dos ficheiros
BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_CONTEXTO_DIR = BASE_DIR / "data" / "raw" / "contexto"

@st.cache_data
def carregar_metricas():
    """Lê diretamente dos ficheiros CSV para alimentar os cartões de métricas."""
    metricas = {
        "populacao_val": "N/D",
        "populacao_delta": "N/D",
        "pib_label": "PIB Real",
        "pib_val": "N/D",
        "pib_delta": "N/D",
        "empregos_val": "N/D",
        "empregos_delta": "N/D",
        "salario_val": "N/D",
        "salario_sub": "N/D"
    }

    # População
    file_pop = PROCESSED_DIR / "populacao_limpo.csv"
    if file_pop.exists():
        df_pop = pd.read_csv(file_pop)
        row_tot = df_pop[df_pop["Faixa Etária"] == "Total General"]
        if not row_tot.empty:
            tot_2022 = int(row_tot["População (2022)"].values[0])
            cresc_pct = float(row_tot["Crescimento (%)"].values[0])
            metricas["populacao_val"] = f"{tot_2022:,.0f}".replace(",", ".") + " hab"
            metricas["populacao_delta"] = f"+{cresc_pct:.2f}% vs 2010"

    # PIB Real
    file_pib = PROCESSED_DIR / "pib_limpo.csv"
    if file_pib.exists():
        df_pib = pd.read_csv(file_pib).sort_values("Ano")
        if not df_pib.empty:
            ult = df_pib.iloc[-1]
            ano_pib = int(ult["Ano"])
            pib_bi = ult["PIB Real 2023 (R$)"] / 1e9
            cresc_pib = ult["Crescimento Real (%)"]
            
            metricas["pib_label"] = f"PIB Real ({ano_pib})"
            metricas["pib_val"] = f"R$ {pib_bi:.2f} Bi"
            if pd.notna(cresc_pib):
                metricas["pib_delta"] = f"{cresc_pib:+.2f}% no ano"

    # Empregos / RAIS / CAGED
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

# --- PÁGINA INICIAL ---
def renderizar_home():
    st.title("📊 Análise Econômica: O Setor de Serviços em Sorocaba-SP")
    st.subheader("Como o setor de serviços influencia o mercado de trabalho local?")

    st.markdown("""
    ---
    ### 🎯 Objetivo do Projeto
    Esta aplicação analisa a estrutura econômica do município de **Sorocaba (SP)**, com foco especial na relevância e no impacto do **Setor de Serviços** sobre a geração de empregos, massa salarial e dinâmica regional.

    #### 🧭 Estrutura da Narrativa
    Use o menu lateral à esquerda para navegar pelas seções da análise.
    ---
    """)

    m = carregar_metricas()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("População (Censo 2022)", m["populacao_val"], m["populacao_delta"])
    col2.metric(m["pib_label"], m["pib_val"], m["pib_delta"])
    col3.metric("Empregos Formais", m["empregos_val"], m["empregos_delta"])
    col4.metric("Salário Médio Formal", m["salario_val"], m["salario_sub"])

# --- DEFINIÇÃO DAS PÁGINAS ---
pagina_home = st.Page(renderizar_home, title="Página Inicial", icon="🏠", default=True)
pagina_contexto = st.Page("pages/01_contexto.py", title="01 — Contexto Econômico", icon="🏙️")

# --- NAVEGAÇÃO NA BARRA LATERAL ---
# Altera a chave da categoria para 'Serviços em Sorocaba'
pg = st.navigation({
    "📊 Serviços em Sorocaba": [
        pagina_home,
        pagina_contexto,
    ]
})

# Executa o Streamlit Navigation
pg.run()
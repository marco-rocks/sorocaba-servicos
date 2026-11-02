import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="01 — Contexto de Sorocaba", page_icon="🏙️", layout="wide")

# Caminhos dos dados processados
BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

st.title("🏙️ Contexto Econômico e Demográfico de Sorocaba")
st.markdown("Análise da evolução do Produto Interno Bruto (PIB Real) e da dinâmica populacional da cidade.")

# --- CARREGAMENTO DOS DADOS ---
@st.cache_data
def carregar_dados():
    df_pib = pd.read_csv(PROCESSED_DIR / "pib_limpo.csv")
    df_pop = pd.read_csv(PROCESSED_DIR / "populacao_limpo.csv")
    return df_pib, df_pop

try:
    df_pib, df_pop = carregar_dados()

    # --- SEÇÃO 1: EVOLUÇÃO DO PIB REAL ---
    st.subheader("📈 Evolução do PIB Real (Preços de 2023)")
    st.markdown("""
    O gráfico abaixo apresenta a trajetória do **PIB Real de Sorocaba**, deflacionado pelo IPCA para valores de 2023. 
    Permite visualizar o crescimento econômico sustentado e a recuperação pós-2020.
    """)

    # Ajuste para R$ bilhões na visualização
    df_pib["PIB_Bi"] = df_pib["PIB Real 2023 (R$)"] / 1e9

    fig_pib = px.line(
        df_pib,
        x="Ano",
        y="PIB_Bi",
        markers=True,
        title="PIB Real de Sorocaba (R$ Bilhões - Preços de 2023)",
        labels={"PIB_Bi": "PIB Real (R$ Bi)", "Ano": "Ano"},
        text=df_pib["PIB_Bi"].apply(lambda x: f"R$ {x:.1f}B")
    )
    
    fig_pib.update_traces(
        line_color="#1f77b4", 
        line_width=3, 
        marker_size=8,
        textposition="top center"
    )
    fig_pib.update_layout(
        xaxis=dict(tickmode="linear", tick0=df_pib["Ano"].min(), dtick=1),
        yaxis_title="R$ Bilhões",
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(fig_pib, use_container_width=True)

    st.markdown("---")

    # --- SEÇÃO 2: ESTRUTURA E CRESCIMENTO POPULACIONAL ---
    st.subheader("👥 Pirâmide e Mudança Etária (Censo 2010 vs 2022)")
    
    # Filtrar a linha do 'Total General' para os gráficos de faixa etária
    df_faixas = df_pop[df_pop["Faixa Etária"] != "Total General"].copy()

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**População por Faixa Etária (2010 vs 2022)**")
        df_melted = df_faixas.melt(
            id_vars=["Faixa Etária"], 
            value_vars=["População (2010)", "População (2022)"],
            var_name="Ano Censo", 
            value_name="Habitantes"
        )
        fig_faixas = px.bar(
            df_melted,
            x="Habitantes",
            y="Faixa Etária",
            color="Ano Censo",
            barmode="group",
            orientation="h",
            height=550,
            title="Comparativo de Habitantes por Faixa Etária"
        )
        st.plotly_chart(fig_faixas, use_container_width=True)

    with col_right:
        st.markdown("**Variação Percentual (%) por Faixa Etária**")
        fig_cresc = px.bar(
            df_faixas,
            x="Crescimento (%)",
            y="Faixa Etária",
            orientation="h",
            color="Crescimento (%)",
            color_continuous_scale="RdBu_r",
            height=550,
            title="Taxa de Crescimento Populacional (2010–2022)"
        )
        st.plotly_chart(fig_cresc, use_container_width=True)

    st.info("""
    💡 **Destaques Demográficos:** 
    - Sorocaba atingiu **723.682 habitantes** no Censo 2022.
    - Observa-se uma nítida transição demográfica: redução nas faixas jovens (10 a 19 anos) e envelhecimento populacional acentuado nas faixas acima de 60 anos.
    """)

except Exception as e:
    st.error(f"Erro ao carregar os dados. Certifique-se de executar `python src/tratamento.py` primeiro. Detalhes: {e}")
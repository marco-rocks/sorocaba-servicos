import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="01 — Contexto de Sorocaba", page_icon="🏙️", layout="wide")

# Caminhos dos dados processados
BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

st.title("🏙️ Contexto Econômico e Demográfico de Sorocaba")
st.markdown("Análise da evolução do Produto Interno Bruto (PIB Real a **preços constantes em 2023**) e da dinâmica populacional com ênfase na transição etária.")

# --- CARREGAMENTO DOS DADOS ---
@st.cache_data
def carregar_dados():
    df_pib = pd.read_csv(PROCESSED_DIR / "pib_limpo.csv")
    df_pop = pd.read_csv(PROCESSED_DIR / "populacao_limpo.csv")
    return df_pib, df_pop

try:
    df_pib, df_pop = carregar_dados()

    # --- SEÇÃO 1: EVOLUÇÃO DO PIB REAL ---
    st.markdown("---")
    st.subheader("📈 Evolução do PIB Real (Preços constantes em 2023)")
    st.markdown("""
    O gráfico abaixo apresenta a trajetória do **PIB Real de Sorocaba**, deflacionado pelo IPCA a **preços constantes em 2023**. 
    Permite visualizar o crescimento econômico sustentado ao longo das últimas duas décadas e a rápida recuperação produtiva no período recente.
    """)

    # Ajuste para R$ bilhões na visualização e formatação brasileira
    df_pib["PIB_Bi"] = df_pib["PIB Real 2023 (R$)"] / 1e9
    df_pib["PIB_Rotulo"] = df_pib["PIB_Bi"].apply(lambda x: f"R$ {x:.2f} Bi".replace(".", ","))

    fig_pib = px.line(
        df_pib,
        x="Ano",
        y="PIB_Bi",
        markers=True,
        title="<b>PIB Real de Sorocaba (R$ Bilhões — Preços constantes em 2023)</b>",
        labels={"PIB_Bi": "PIB Real (R$ Bilhões)", "Ano": "Ano"},
        text="PIB_Rotulo"
    )
    
    fig_pib.update_traces(
        line_color="#1f77b4", 
        line_width=3, 
        marker_size=8,
        textposition="top center"
    )
    fig_pib.update_layout(
        title_font_size=16,
        xaxis=dict(tickmode="linear", tick0=int(df_pib["Ano"].min()), dtick=1),
        yaxis_title="PIB Real (R$ Bilhões)",
        height=480,
        hovermode="x unified"
    )

    st.plotly_chart(fig_pib, use_container_width=True)
    st.caption("Fonte: IBGE / Fundação SEADE — Série histórica deflacionada pelo IPCA (preços constantes em 2023).")

    st.markdown("---")

    # --- SEÇÃO 2: ESTRUTURA E CRESCIMENTO POPULACIONAL ---
    st.subheader("👥 Estrutura Demográfica e Variação Etária (Censo 2010 vs 2022)")
    st.markdown("""
    Abaixo evidencia-se a transição da pirâmide etária do município. As porcentagens de crescimento por faixa de idade ilustram o 
    envelhecimento demográfico acentuado e a diminuição de coortes mais jovens, fenômeno que altera a oferta e a demanda de serviços (saúde, lazer e educação).
    """)

    # Filtrar a linha do 'Total General' para os gráficos de faixa etária
    df_faixas = df_pop[df_pop["Faixa Etária"] != "Total General"].copy()

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("##### 📊 População Absoluta por Faixa Etária (2010 vs 2022)")
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
            height=580,
            title="<b>Comparativo Absoluto de Habitantes por Faixa Etária</b>",
            color_discrete_map={"População (2010)": "#9ecae1", "População (2022)": "#1f77b4"}
        )
        fig_faixas.update_layout(
            title_font_size=15,
            separators=",.",
            xaxis=dict(tickformat=".")
        )
        st.plotly_chart(fig_faixas, use_container_width=True)
        st.caption("Fonte: IBGE — Censos Demográficos 2010 e 2022.")

    with col_right:
        st.markdown("##### 🎯 Variação Percentual (%) por Faixa Etária — Ênfase na Idade")
        df_faixas["Texto_Pct"] = df_faixas["Crescimento (%)"].apply(lambda v: f"{v:+.1f}%".replace(".", ","))
        
        fig_cresc = px.bar(
            df_faixas,
            x="Crescimento (%)",
            y="Faixa Etária",
            orientation="h",
            color="Crescimento (%)",
            color_continuous_scale="RdBu_r",
            height=580,
            title="<b>Taxa de Crescimento (%) por Faixa Etária (2010 a 2022)</b>",
            text="Texto_Pct"
        )
        fig_cresc.update_traces(
            textposition="outside",
            textfont=dict(size=12, color="black")
        )
        fig_cresc.update_layout(
            title_font_size=15,
            xaxis=dict(title="Variação Percentual (%)", dtick=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_cresc, use_container_width=True)
        st.caption("Fonte: Elaboração própria com dados do IBGE (Censos 2010 e 2022).")

    # Destaques demográficos com ênfase nas faixas
    tot_row = df_pop[df_pop["Faixa Etária"] == "Total General"]
    tot_2022_str = "723.682"
    if not tot_row.empty:
        tot_2022_str = f"{int(tot_row['População (2022)'].values[0]):,}".replace(",", ".")

    st.info(f"""
    💡 **Destaques Demográficos com Ênfase nas Porcentagens Etárias:** 
    - **População Total:** Sorocaba atingiu **{tot_2022_str} habitantes** em 2022, expansão global de **+23,36%** sobre 2010.
    - **Envelhecimento Acentuado:** As faixas seniores apresentaram os maiores saltos relativos da história do município:
        - **80 anos ou mais:** salto de **+105,7%** (mais que dobrou o contingente de idosos longevos).
        - **70 a 74 anos:** alta de **+89,8%**.
        - **65 a 69 anos:** expansão de **+80,8%**.
        - **60 a 64 anos:** crescimento de **+66,2%**.
    - **Redução nas Coortes Jovens:** Houve contração populacional nas idades de formação básica e entrada no ensino médio:
        - **10 a 14 anos:** retração de **-7,15%**.
        - **15 a 19 anos:** recuo de **-4,62%**.
    - **Impacto no Setor Terciário:** Esse perfil reorienta o mercado de trabalho, ampliando a demanda por serviços médicos, cuidados de saúde, clínicas integradas, geriatria, farmácias, seguros e entretenimento adulto.
    """)

except Exception as e:
    st.error(f"Erro ao carregar os dados. Certifique-se de executar `python src/tratamento.py` primeiro. Detalhes: {e}")

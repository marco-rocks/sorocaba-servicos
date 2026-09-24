import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="02 — Mercado de Trabalho", 
    page_icon="💼", 
    layout="wide"
)

# Definir caminho relativo para a pasta de dados processados
BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

st.title("💼 Estrutura do Mercado de Trabalho Formal")
st.markdown("Análise da evolução temporal do número de empresas, postos de trabalho e massa salarial em Sorocaba (Fonte: CEMPRE/IBGE).")

@st.cache_data
def carregar_dados():
    filepath = PROCESSED_DIR / "empresas_empregos_limpo.csv"
    if not filepath.exists():
        return None
    return pd.read_csv(filepath)

try:
    df_emp = carregar_dados()

    if df_emp is None:
        st.error("⚠️ O ficheiro `empresas_empregos_limpo.csv` não foi encontrado em `data/processed/`. Por favor, execute primeiro o script `python src/tratamento.py`.")
    else:
        # Ordenar a série histórica por ano
        df_emp = df_emp.sort_values("Ano").reset_index(drop=True)

        ult_linha = df_emp.iloc[-1]
        pri_linha = df_emp.iloc[0]

        ano_ult = int(ult_linha["Ano"])
        ano_pri = int(pri_linha["Ano"])

        cresc_pessoal = ((ult_linha["Pessoal Ocupado"] - pri_linha["Pessoal Ocupado"]) / pri_linha["Pessoal Ocupado"]) * 100
        cresc_empresas = ((ult_linha["Empresas"] - pri_linha["Empresas"]) / pri_linha["Empresas"]) * 100

        # --- SEÇÃO DE CARDS DE MÉTRICAS ---
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric(
            label=f"Pessoal Ocupado ({ano_ult})", 
            value=f"{int(ult_linha['Pessoal Ocupado']):,}".replace(",", "."), 
            delta=f"+{cresc_pessoal:.1f}% vs {ano_pri}"
        )
        col2.metric(
            label=f"Empresas Formais ({ano_ult})", 
            value=f"{int(ult_linha['Empresas']):,}".replace(",", "."), 
            delta=f"+{cresc_empresas:.1f}% vs {ano_pri}"
        )
        col3.metric(
            label=f"Pessoal Assalariado ({ano_ult})", 
            value=f"{int(ult_linha['Pessoal Assalariado']):,}".replace(",", ".")
        )
        col4.metric(
            label=f"Salário Médio ({ano_ult})", 
            value=f"{ult_linha['Salário Médio (S.M.)']:.1f} S.M."
        )

        st.markdown("---")

        # --- GRÁFICO 1: EVOLUÇÃO DO EMPREGO FORMAL ---
        st.subheader("📈 Trajetória do Emprego Formal (2006 – 2021)")
        st.markdown("Comparativo entre o volume total de **Pessoal Ocupado** (inclui sócios e proprietários) e o **Pessoal Assalariado**.")

        df_melt = df_emp.melt(
            id_vars=["Ano"],
            value_vars=["Pessoal Ocupado", "Pessoal Assalariado"],
            var_name="Tipo de Vínculo",
            value_name="Trabalhadores"
        )

        fig_emp = px.line(
            df_melt,
            x="Ano",
            y="Trabalhadores",
            color="Tipo de Vínculo",
            markers=True,
            title="Evolução do Pessoal Ocupado Total vs. Pessoal Assalariado",
            labels={"Trabalhadores": "Número de Pessoas", "Ano": "Ano"}
        )
        fig_emp.update_traces(line_width=3, marker_size=7)
        fig_emp.update_layout(
            xaxis=dict(dtick=1, tickmode="linear"),
            height=420,
            hovermode="x unified"
        )
        st.plotly_chart(fig_emp, use_container_width=True)

        st.markdown("---")

        # --- PAINEL DUPLO: EMPRESAS E SALÁRIOS ---
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("🏢 Crescimento do Total de Empresas")
            fig_emp_bar = px.bar(
                df_emp,
                x="Ano",
                y="Empresas",
                text="Empresas",
                title="Empresas Formais Ativas em Sorocaba",
                labels={"Empresas": "Qtd. de Empresas", "Ano": "Ano"},
                color_discrete_sequence=["#1f77b4"]
            )
            fig_emp_bar.update_traces(textposition="outside")
            fig_emp_bar.update_layout(
                xaxis=dict(dtick=1, tickmode="linear"), 
                height=400
            )
            st.plotly_chart(fig_emp_bar, use_container_width=True)

        with col_r:
            st.subheader("💵 Evolução da Remuneração Média")
            fig_sal = px.line(
                df_emp,
                x="Ano",
                y="Salário Médio (S.M.)",
                markers=True,
                title="Salário Médio Mensal em Salários Mínimos (S.M.)",
                labels={"Salário Médio (S.M.)": "Salários Mínimos", "Ano": "Ano"},
                color_discrete_sequence=["#2ca02c"]
            )
            fig_sal.update_traces(line_width=3, marker_size=8)
            fig_sal.update_layout(
                xaxis=dict(dtick=1, tickmode="linear"), 
                height=400
            )
            st.plotly_chart(fig_sal, use_container_width=True)

        # --- PAINEL DE SÍNTESE ---
        st.info("""
        💡 **Destaques do Mercado de Trabalho Formal:**
        - **Crescimento do Emprego:** O pessoal ocupado saltou de **156,1 mil** (2006) para **237,3 mil** (2021), representando uma expansão acumulada de **+52,0%**.
        - **Expansão Empresarial:** O tecido empresarial formal cresceu de **18,5 mil** para **29,4 mil** empresas ativas no mesmo período (+59,1%).
        - **Massa Salarial e Renda:** O salário médio formal permaneceu em patamares acima de 4,0 Salários Mínimos até 2014, ajustando-se gradualmente para 3,8 S.M. nos anos mais recentes.
        """)

except Exception as e:
    st.error(f"Erro ao processar a página: {e}")
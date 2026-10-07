import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="03 — Setor de Serviços", 
    page_icon="🛎️", 
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"

st.title("🛎️ Estrutura do Setor de Serviços")
st.markdown("Análise da evolução temporal das empresas e empregos no setor de serviços em Sorocaba (Fonte: SIDRA/IBGE).")

@st.cache_data
def carregar_dados():
    df_unid = pd.read_csv(DATA_DIR / "unidades_servicos.csv", sep=";")
    df_pess = pd.read_csv(DATA_DIR / "pessoas_servicos.csv", sep=";")

    # --- RENOMEAR PARA PADRÃO ANTIGO ---
    df_unid = df_unid.rename(columns={
        "ano": "Ano",
        "tipo": "Tipo",
        "qtd_empresa": "Unidades"
    })

    df_pess = df_pess.rename(columns={
        "ano": "ano",
        "tipo": "Tipo",
        "qtd_pessoas": "qtd_pessoas"
    })

    return df_unid, df_pess

try:
    df_unid, df_pess = carregar_dados()

    # --- TRATAMENTO ---
    df_unid = df_unid[df_unid["Unidades"].apply(lambda x: str(x).isdigit())]
    df_unid["Unidades"] = df_unid["Unidades"].astype(int)

    df_pess = df_pess[df_pess["qtd_pessoas"].apply(lambda x: str(x).isdigit())]
    df_pess["qtd_pessoas"] = df_pess["qtd_pessoas"].astype(int)

    # --- NORMALIZAÇÃO DO NOME DO SUBSETOR ---
    df_unid["Tipo"] = df_unid["Tipo"].str.replace(r"^\s*\d+(\.\d+)*-?\d*\s*", "", regex=True).str.strip()
    df_pess["Tipo"] = df_pess["Tipo"].str.replace(r"^\s*\d+(\.\d+)*-?\d*\s*", "", regex=True).str.strip()

    # --- DEDUPLICAÇÃO POR NOME ---
    df_unid = df_unid.groupby(["Ano", "Tipo"], as_index=False)["Unidades"].sum()
    df_pess = df_pess.groupby(["ano", "Tipo"], as_index=False)["qtd_pessoas"].sum()

    # Totais por ano
    total_empresas = df_unid.groupby("Ano")["Unidades"].sum().reset_index()
    total_pessoas = df_pess.groupby("ano")["qtd_pessoas"].sum().reset_index()

    # --- MÉTRICAS ---
    col1, col2 = st.columns(2)
    col1.metric("Total de Empresas (2024)", f"{total_empresas.loc[total_empresas['Ano']==2024,'Unidades'].values[0]:,}".replace(",", "."))
    col2.metric("Total de Pessoas Ocupadas (2024)", f"{total_pessoas.loc[total_pessoas['ano']==2024,'qtd_pessoas'].values[0]:,}".replace(",", "."))

    st.markdown("---")

    # --- EVOLUÇÃO EMPRESAS ---
    st.subheader("🏢 Evolução do Número de Empresas de Serviços")
    fig_emp = px.line(total_empresas, x="Ano", y="Unidades", markers=True,
        title="Total de Empresas de Serviços (2006–2024)",
        labels={"Unidades": "Qtd. de Empresas", "Ano": "Ano"})
    fig_emp.update_traces(line_color="#1f77b4", line_width=4,
        marker=dict(size=10, symbol="circle", line=dict(width=2, color="black")))
    fig_emp.update_layout(xaxis=dict(tickmode="linear", dtick=1), height=600, hovermode="x unified")
    st.plotly_chart(fig_emp, use_container_width=True)
    st.caption("Fonte dos dados: SIDRA/IBGE")

    # --- EVOLUÇÃO PESSOAL OCUPADO ---
    st.subheader("👥 Evolução do Pessoal Ocupado em Serviços")
    fig_pess = px.line(total_pessoas, x="ano", y="qtd_pessoas", markers=True,
        title="Total de Pessoas Ocupadas em Serviços (2006–2024)",
        labels={"qtd_pessoas": "Número de Pessoas", "ano": "Ano"})
    fig_pess.update_traces(line_color="#2ca02c", line_width=4,
        marker=dict(size=10, symbol="diamond", line=dict(width=2, color="black")))
    fig_pess.update_layout(xaxis=dict(tickmode="linear", dtick=1), height=600, hovermode="x unified")
    st.plotly_chart(fig_pess, use_container_width=True)
    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # --- COMPARATIVO EMPRESAS VS PESSOAL ---
    st.subheader("📊 Comparativo: Empresas vs Pessoal Ocupado")
    df_comp = pd.merge(total_empresas, total_pessoas, left_on="Ano", right_on="ano")
    fig_comp = px.bar(df_comp, x="Ano", y=["Unidades", "qtd_pessoas"],
        barmode="group", title="Empresas vs Pessoas Ocupadas",
        labels={"value": "Quantidade", "Ano": "Ano", "variable": "Indicador"})
    st.plotly_chart(fig_comp, use_container_width=True)
    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # --- DISTRIBUIÇÃO POR SUBSETORES ---
    st.subheader("📌 Distribuição de Empresas por Subsetor (2024)")
    df_unid_2024 = df_unid[df_unid["Ano"]==2024].sort_values("Unidades", ascending=False).head(10)
    fig_top_emp = px.bar(df_unid_2024, x="Tipo", y="Unidades", text="Unidades",
        title="Top 10 Subsetores em Número de Empresas (2024)",
        labels={"Unidades": "Qtd. de Empresas", "Tipo": "Subsetor"},
        color="Unidades", color_continuous_scale="Blues")
    fig_top_emp.update_traces(textposition="outside")
    fig_top_emp.update_layout(height=700, font=dict(size=14), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig_top_emp, use_container_width=True)
    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.subheader("👥 Distribuição de Empregos por Subsetor (2024)")
    df_pess_2024 = df_pess[df_pess["ano"]==2024].sort_values("qtd_pessoas", ascending=False).head(10)
    fig_top_pess = px.bar(df_pess_2024, x="Tipo", y="qtd_pessoas", text="qtd_pessoas",
        title="Top 10 Subsetores em Número de Pessoas Ocupadas (2024)",
        labels={"qtd_pessoas": "Qtd. de Pessoas", "Tipo": "Subsetor"},
        color="qtd_pessoas", color_continuous_scale="Greens")
    fig_top_pess.update_traces(textposition="outside")
    fig_top_pess.update_layout(height=700, font=dict(size=14), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig_top_pess, use_container_width=True)
    st.caption("Fonte dos dados: SIDRA/IBGE")
    st.markdown("---")

    # --- TAXA DE CRESCIMENTO POR SUBSETORES ---
    st.subheader("📈 Crescimento por Subsetor (2014–2024)")
    df_cresc = df_unid.groupby("Tipo").agg(
        emp_2014=("Unidades", lambda x: x[df_unid.loc[x.index,"Ano"]==2014].sum()),
        emp_2024=("Unidades", lambda x: x[df_unid.loc[x.index,"Ano"]==2024].sum())
    ).reset_index()
    df_cresc["crescimento_%"] = ((df_cresc["emp_2024"] - df_cresc["emp_2014"]) / df_cresc["emp_2014"]) * 100
    df_cresc = df_cresc.sort_values("crescimento_%", ascending=False).head(10)

    fig_cresc = px.bar(df_cresc, x="Tipo", y="crescimento_%", text="crescimento_%",
        title="Top 10 Subsetores em Crescimento de Empresas (2014–2024)",
        labels={"crescimento_%": "Crescimento (%)", "Tipo": "Subsetor"},
        color="crescimento_%", color_continuous_scale="RdYlGn")
    fig_cresc.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_cresc.update_layout(height=700, font=dict(size=14), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig_cresc, use_container_width=True)
    st.caption("Fonte dos dados: SIDRA/IBGE")

except Exception as e:
    st.error(f"Erro ao processar a página: {e}")

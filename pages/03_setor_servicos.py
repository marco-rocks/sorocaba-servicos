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

MUNICIPIO = "Sorocaba"
ANO_INICIO_NEGOCIOS = 2006  # mesma janela inicial da versão anterior da página

st.title("🛎️ Estrutura do Setor de Serviços")
st.markdown("Análise da evolução temporal das empresas e empregos no setor de serviços em Sorocaba (Fonte: base de estabelecimentos e empregados por divisão econômica).")

def encurtar(txt, limite=38):
    """Encurta nomes longos de divisão para caber no eixo X (nome completo fica no hover)."""
    txt = str(txt)
    return txt if len(txt) <= limite else txt[:limite - 1].rstrip() + "…"

@st.cache_data
def carregar_dados():
    df_unid = pd.read_csv(DATA_DIR / "estabelecimentos_servicos.csv", sep=";")
    df_pess = pd.read_csv(DATA_DIR / "pessoas_servicos.csv", sep=";")
    df_novos = pd.read_csv(DATA_DIR / "novos_negocios.csv", sep=";")
    df_tot = pd.read_csv(DATA_DIR / "empregados_total_municipios.csv", sep=";")

    # --- PADRONIZAÇÃO DE NOMES (mantém o padrão usado nos gráficos) ---
    df_unid = df_unid.rename(columns={"tipo": "Tipo", "qtd_empresa": "Unidades"})
    df_pess = df_pess.rename(columns={"tipo": "Tipo"})
    df_novos = df_novos.rename(columns={"ano": "Ano", "qtd_empresa": "Unidades"})
    df_tot = df_tot[df_tot["municipio"] == MUNICIPIO].rename(columns={"ano": "Ano"})

    return df_unid, df_pess, df_novos, df_tot

try:
    df_unid, df_pess, df_novos, df_tot = carregar_dados()

    # --- TRATAMENTO ---
    df_unid["Unidades"] = pd.to_numeric(df_unid["Unidades"], errors="coerce")
    df_unid = df_unid.dropna(subset=["Unidades"])
    df_unid["Unidades"] = df_unid["Unidades"].astype(int)

    df_pess["qtd_pessoas"] = pd.to_numeric(df_pess["qtd_pessoas"], errors="coerce")
    df_pess = df_pess.dropna(subset=["qtd_pessoas"])
    df_pess["qtd_pessoas"] = df_pess["qtd_pessoas"].astype(int)

    # --- DEDUPLICAÇÃO POR NOME ---
    df_unid = df_unid.groupby("Tipo", as_index=False)["Unidades"].sum()
    df_pess = df_pess.groupby(["ano", "Tipo"], as_index=False)["qtd_pessoas"].sum()

    # Totais por ano
    # Empresas: novos negócios abertos por ano (todos os setores) — a nova base não traz
    # série histórica de estabelecimentos ativos por setor.
    total_empresas = (
        df_novos[df_novos["Ano"] >= ANO_INICIO_NEGOCIOS]
        .groupby("Ano")["Unidades"].sum().reset_index()
    )
    total_pessoas = df_pess.groupby("ano")["qtd_pessoas"].sum().reset_index()

    ano_pess = int(total_pessoas["ano"].max())

    # --- MÉTRICAS ---
    col1, col2 = st.columns(2)
    col1.metric("Total de Estabelecimentos Ativos em Serviços", f"{int(df_unid['Unidades'].sum()):,}".replace(",", "."))
    col2.metric(f"Total de Empregados em Serviços ({ano_pess})", f"{total_pessoas.loc[total_pessoas['ano']==ano_pess,'qtd_pessoas'].values[0]:,}".replace(",", "."))

    st.markdown("---")

    # --- EVOLUÇÃO EMPRESAS ---
    st.subheader("🏢 Evolução do Número de Empresas (Novos Negócios por Ano de Abertura)")
    fig_emp = px.line(total_empresas, x="Ano", y="Unidades", markers=True,
        title=f"Novos Negócios Abertos por Ano — todos os setores ({total_empresas['Ano'].min()}–{total_empresas['Ano'].max()})",
        labels={"Unidades": "Qtd. de Empresas", "Ano": "Ano"})
    fig_emp.update_traces(line_color="#1f77b4", line_width=4,
        marker=dict(size=10, symbol="circle", line=dict(width=2, color="black")))
    fig_emp.update_layout(xaxis=dict(tickmode="linear", dtick=1), height=600, hovermode="x unified")
    st.plotly_chart(fig_emp, use_container_width=True)
    st.caption(
        "Fonte dos dados: base de novos negócios (todos os setores; não há recorte só de serviços). "
        "Considera apenas estabelecimentos hoje ativos, por ano de abertura; o último ano pode estar incompleto."
    )

    # --- EVOLUÇÃO PESSOAL OCUPADO ---
    st.subheader("👥 Evolução do Pessoal Ocupado em Serviços")
    fig_pess = px.line(total_pessoas, x="ano", y="qtd_pessoas", markers=True,
        title=f"Total de Empregados em Serviços ({total_pessoas['ano'].min()}–{total_pessoas['ano'].max()})",
        labels={"qtd_pessoas": "Número de Pessoas", "ano": "Ano"})
    fig_pess.update_traces(line_color="#2ca02c", line_width=4,
        marker=dict(size=10, symbol="diamond", line=dict(width=2, color="black")))
    fig_pess.update_layout(xaxis=dict(tickmode="linear", dtick=1), height=600, hovermode="x unified")
    st.plotly_chart(fig_pess, use_container_width=True)
    st.caption("Fonte dos dados: base de empregados por divisão econômica (setor Serviços)")

    st.markdown("---")

    # --- COMPARATIVO EMPRESAS VS PESSOAL ---
    st.subheader("📊 Comparativo: Empresas vs Pessoal Ocupado")
    # Mesmo escopo nos dois indicadores (todos os setores do município)
    df_comp = pd.merge(
        total_empresas.rename(columns={"Unidades": "Novos negócios"}),
        df_tot[["Ano", "empregados_total"]].rename(columns={"empregados_total": "Empregados (total do município)"}),
        on="Ano"
    )
    fig_comp = px.bar(df_comp, x="Ano", y=["Novos negócios", "Empregados (total do município)"],
        barmode="group", title="Novos Negócios vs Empregados (todos os setores)",
        labels={"value": "Quantidade", "Ano": "Ano", "variable": "Indicador"})
    st.plotly_chart(fig_comp, use_container_width=True)
    st.caption("Fonte dos dados: bases de novos negócios e de empregados totais do município (todos os setores)")

    st.markdown("---")

    # --- DISTRIBUIÇÃO POR SUBSETORES ---
    st.subheader("📌 Distribuição de Empresas por Subsetor (Estabelecimentos Ativos)")
    df_unid_top = df_unid.sort_values("Unidades", ascending=False).head(10).copy()
    df_unid_top["Tipo_curto"] = df_unid_top["Tipo"].apply(encurtar)
    fig_top_emp = px.bar(df_unid_top, x="Tipo_curto", y="Unidades", text="Unidades",
        hover_name="Tipo",
        title="Top 10 Subsetores em Número de Empresas (estabelecimentos ativos)",
        labels={"Unidades": "Qtd. de Empresas", "Tipo_curto": "Subsetor"},
        color="Unidades", color_continuous_scale="Blues")
    fig_top_emp.update_traces(textposition="outside")
    fig_top_emp.update_layout(height=700, font=dict(size=14), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig_top_emp, use_container_width=True)
    st.caption("Fonte dos dados: base de estabelecimentos ativos por divisão econômica (posição atual, sem recorte por ano)")

    st.subheader(f"👥 Distribuição de Empregos por Subsetor ({ano_pess})")
    df_pess_top = df_pess[df_pess["ano"]==ano_pess].sort_values("qtd_pessoas", ascending=False).head(10).copy()
    df_pess_top["Tipo_curto"] = df_pess_top["Tipo"].apply(encurtar)
    fig_top_pess = px.bar(df_pess_top, x="Tipo_curto", y="qtd_pessoas", text="qtd_pessoas",
        hover_name="Tipo",
        title=f"Top 10 Subsetores em Número de Pessoas Ocupadas ({ano_pess})",
        labels={"qtd_pessoas": "Qtd. de Pessoas", "Tipo_curto": "Subsetor"},
        color="qtd_pessoas", color_continuous_scale="Greens")
    fig_top_pess.update_traces(textposition="outside")
    fig_top_pess.update_layout(height=700, font=dict(size=14), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig_top_pess, use_container_width=True)
    st.caption("Fonte dos dados: base de empregados por divisão econômica (setor Serviços)")
    st.markdown("---")

    # --- TAXA DE CRESCIMENTO POR SUBSETORES ---
    ano_ini = int(df_pess["ano"].min())
    st.subheader(f"📈 Crescimento por Subsetor ({ano_ini}–{ano_pess})")
    # A base de estabelecimentos não tem série histórica; o crescimento é medido em empregados.
    # Só entram subsetores presentes nos dois anos e com base mínima de 100 empregados no ano inicial.
    ini = df_pess[df_pess["ano"] == ano_ini][["Tipo", "qtd_pessoas"]].rename(columns={"qtd_pessoas": "emp_inicio"})
    fim = df_pess[df_pess["ano"] == ano_pess][["Tipo", "qtd_pessoas"]].rename(columns={"qtd_pessoas": "emp_fim"})
    df_cresc = ini.merge(fim, on="Tipo")
    df_cresc = df_cresc[df_cresc["emp_inicio"] >= 100].copy()
    df_cresc["crescimento_%"] = ((df_cresc["emp_fim"] - df_cresc["emp_inicio"]) / df_cresc["emp_inicio"]) * 100
    df_cresc = df_cresc.sort_values("crescimento_%", ascending=False).head(10)
    df_cresc["Tipo_curto"] = df_cresc["Tipo"].apply(encurtar)

    fig_cresc = px.bar(df_cresc, x="Tipo_curto", y="crescimento_%", text="crescimento_%",
        hover_name="Tipo",
        title=f"Top 10 Subsetores em Crescimento de Empregos ({ano_ini}–{ano_pess})",
        labels={"crescimento_%": "Crescimento (%)", "Tipo_curto": "Subsetor"},
        color="crescimento_%", color_continuous_scale="RdYlGn")
    fig_cresc.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_cresc.update_layout(height=700, font=dict(size=14), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig_cresc, use_container_width=True)
    st.caption("Fonte dos dados: base de empregados por divisão econômica (setor Serviços)")

except Exception as e:
    st.error(f"Erro ao processar a página: {e}")
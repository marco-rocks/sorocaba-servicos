import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="04 — Salários e Ocupações",
    page_icon="💼",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"

st.title("💼 Salários e Ocupações")
st.markdown(
    """
    Análise das ocupações formais, quantidade de trabalhadores e
    remuneração média com base nos dados da RAIS.

    Fonte dos dados: CBO
    """
)

# ==========================================================
# CARREGAMENTO DOS DADOS
# ==========================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_DIR / "rais_ocupacoes_limpo.csv")

    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["trabalhadores"] = pd.to_numeric(df["trabalhadores"], errors="coerce")
    df["salario_medio"] = pd.to_numeric(df["salario_medio"], errors="coerce")

    df = df.dropna(
        subset=[
            "ano",
            "ocupacao",
            "trabalhadores",
            "salario_medio"
        ]
    )

    df["ano"] = df["ano"].astype(int)

    return df

def formatar_real(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


try:

    df = carregar_dados()

    if df.empty:
        st.warning("Nenhum dado encontrado.")
        st.stop()

    # ==========================================================
    # FILTRO DE ANO
    # ==========================================================

    anos = sorted(df["ano"].unique(), reverse=True)

    anos_opcoes = ["Todos"] + list(anos)

    ano_sel = st.selectbox(
        "Selecione o ano",
        anos_opcoes
    )

    if ano_sel == "Todos":

        df_ano = (
            df.groupby(
                ["codigo_cbo", "ocupacao"],
                as_index=False
            )
            .agg(
                trabalhadores=("trabalhadores", "sum"),
                salario_medio=("salario_medio", "mean")
            )
        )

    else:

        df_ano = (
            df[df["ano"] == ano_sel]
            .copy()
        )

    if df_ano.empty:
        st.warning("Nenhum dado encontrado para o filtro selecionado.")
        st.stop()

    # ==========================================================
    # MÉTRICAS
    # ==========================================================

    total_trabalhadores = df_ano["trabalhadores"].sum()

    salario_ponderado = (
        (df_ano["salario_medio"] * df_ano["trabalhadores"]).sum()
        / total_trabalhadores
    )

    ocupacao_lider = (
        df_ano
        .sort_values("trabalhadores", ascending=False)
        .iloc[0]["ocupacao"]
    )

    qtd_ocupacoes = df_ano["ocupacao"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Trabalhadores",
        f"{total_trabalhadores:,.0f}".replace(",", ".")
    )

    col2.metric(
    "💰 Salário Médio",
    formatar_real(salario_ponderado)

    )

    col3.metric(
        "📋 Ocupações",
        f"{qtd_ocupacoes:,}".replace(",", ".")
    )

    col4.metric(
        "🏆 Maior Ocupação",
        ocupacao_lider
    )

    st.markdown("---")

    # ==========================================================
    # TOP 15 OCUPAÇÕES
    # ==========================================================

    st.subheader("👷 Top 15 Ocupações por Número de Trabalhadores")

    top_trabalhadores = (
        df_ano
        .sort_values("trabalhadores", ascending=False)
        .head(15)
    )

    fig_top = px.bar(
        top_trabalhadores,
        y="ocupacao",
        x="trabalhadores",
        orientation="h",
        text="trabalhadores",
        color="trabalhadores",
        color_continuous_scale="Blues"
    )

    fig_top.update_layout(
        height=700,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig_top, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # TOP SALÁRIOS
    # ==========================================================

    st.subheader("💰 Top 15 Ocupações por Salário Médio")

    top_salarios = (
        df_ano[df_ano["trabalhadores"] >= 30]
        .sort_values("salario_medio", ascending=False)
        .head(15)
    )

    top_salarios = top_salarios.copy()

    top_salarios["salario_formatado"] = (
        top_salarios["salario_medio"]
        .apply(formatar_real)
    )

    fig_salarios = px.bar(
        top_salarios,
        y="ocupacao",
        x="salario_medio",
        orientation="h",
        text="salario_formatado",
        color="salario_medio",
        color_continuous_scale="Greens"
    )

    fig_salarios.update_traces(
    hovertemplate=
    "<b>%{y}</b><br>" +
    "Salário Médio: R$ %{x:,.2f}<extra></extra>"
    )
    

    fig_salarios.update_layout(
        height=700,
        yaxis=dict(categoryorder="total ascending"),
        xaxis_tickprefix="R$ ",
    )

    st.plotly_chart(fig_salarios, use_container_width=True)


    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # MASSA SALARIAL
    # ==========================================================

    st.subheader("💵 Top 15 Ocupações por Massa Salarial")

    df_massa = df_ano.copy()

    df_massa["massa_salarial"] = (
        df_massa["trabalhadores"]
        * df_massa["salario_medio"]
    )

    top_massa = (
        df_massa
        .sort_values("massa_salarial", ascending=False)
        .head(15)
    )

    top_massa = top_massa.copy()

    top_massa["massa_formatada"] = (
        top_massa["massa_salarial"]
        .apply(formatar_real)
     )

    fig_massa = px.bar(
        top_massa,
        x="ocupacao",
        y="massa_salarial",
        text="massa_formatada",
        color="massa_salarial",
        color_continuous_scale="Oranges"
    )

    fig_massa.update_traces(
        hovertemplate=
        "<b>%{x}</b><br>" +
        "Massa Salarial: R$ %{y:,.2f}<extra></extra>"
    )

    fig_massa.update_layout(
        height=700,
        xaxis_tickangle=-35,
        yaxis_tickprefix="R$ ",
    )

    st.plotly_chart(fig_massa, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # SCATTER
    # ==========================================================

    st.subheader(
        "📊 Relação entre Salário Médio e Número de Trabalhadores"
    )

    scatter_df = df_ano[df_ano["trabalhadores"] >= 30]

    fig_scatter = px.scatter(
        scatter_df,
        x="trabalhadores",
        y="salario_medio",
        size="trabalhadores",
        color="salario_medio",
        hover_name="ocupacao",
        hover_data=["codigo_cbo"],
        color_continuous_scale="Viridis"
    )

    fig_scatter.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br>" +
        "Trabalhadores: %{x:,}<br>" +
        "Salário Médio: R$ %{y:,.2f}<extra></extra>"
    )

    fig_scatter.update_layout(
        height=700
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # EVOLUÇÃO DOS TRABALHADORES
    # ==========================================================

    st.subheader("📈 Evolução do Total de Trabalhadores")

    evol_trab = (
        df.groupby("ano", as_index=False)["trabalhadores"]
        .sum()
    )

    fig_evol_trab = px.line(
        evol_trab,
        x="ano",
        y="trabalhadores",
        markers=True
    )

    fig_evol_trab.update_traces(
        line_width=4,
        marker_size=10
    )

    fig_evol_trab.update_layout(
        height=600,
        hovermode="x unified",
        xaxis=dict(
            tickmode="linear",
            dtick=1
        )
    )

    st.plotly_chart(fig_evol_trab, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # EVOLUÇÃO SALÁRIO MÉDIO
    # ==========================================================

    st.subheader("💰 Evolução do Salário Médio")

    evol_salario = (
        df.groupby("ano")
        .apply(
            lambda x: (
                (x["salario_medio"] * x["trabalhadores"]).sum()
                / x["trabalhadores"].sum()
            )
        )
        .reset_index(name="salario_medio")
    )

    fig_evol_sal = px.line(
        evol_salario,
        x="ano",
        y="salario_medio",
        markers=True
    )

    fig_evol_sal.update_traces(
        line_width=4,
        hovertemplate=
        "<b>Ano: %{x}</b><br>" +
        "Salário Médio: R$ %{y:,.2f}<extra></extra>"
    )

    fig_evol_sal.update_layout(
        height=600,
        hovermode="x unified",
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        yaxis_tickprefix="R$ "
    )

    st.plotly_chart(fig_evol_sal, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # CRESCIMENTO ANUAL
    # ==========================================================

    st.subheader("🚀 Crescimento Anual dos Trabalhadores")

    crescimento = evol_trab.copy()

    crescimento["crescimento_%"] = (
        crescimento["trabalhadores"]
        .pct_change()
        * 100
    )

    fig_crescimento = px.bar(
        crescimento,
        x="ano",
        y="crescimento_%",
        text="crescimento_%",
        color="crescimento_%",
        color_continuous_scale="RdYlGn"
    )

    fig_crescimento.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig_crescimento.update_layout(
        height=600
    )

    st.plotly_chart(fig_crescimento, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # OCUPAÇÕES QUE MAIS CRESCERAM
    # ==========================================================

    st.subheader("🏆 Ocupações que Mais Cresceram")

    ano_inicial = df["ano"].min()
    ano_final = df["ano"].max()

    inicio = (
        df[df["ano"] == ano_inicial]
        [["ocupacao", "trabalhadores"]]
        .rename(columns={"trabalhadores": "inicio"})
    )

    fim = (
        df[df["ano"] == ano_final]
        [["ocupacao", "trabalhadores"]]
        .rename(columns={"trabalhadores": "fim"})
    )

    crescimento_ocup = inicio.merge(
        fim,
        on="ocupacao"
    )

    crescimento_ocup = crescimento_ocup[
        crescimento_ocup["inicio"] >= 50
    ]

    crescimento_ocup["crescimento_%"] = (
        (crescimento_ocup["fim"] - crescimento_ocup["inicio"])
        / crescimento_ocup["inicio"]
    ) * 100

    crescimento_ocup = crescimento_ocup.sort_values(
        "crescimento_%",
        ascending=False
    ).head(15)

    fig_ocup = px.bar(
        crescimento_ocup,
        x="ocupacao",
        y="crescimento_%",
        text="crescimento_%",
        color="crescimento_%",
        color_continuous_scale="RdYlGn"
    )

    fig_ocup.update_traces(
        texttemplate="%{text:.1f}%"
    )

    fig_ocup.update_layout(
        height=700,
        xaxis_tickangle=-35
    )

    st.plotly_chart(fig_ocup, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

    st.markdown("---")

    # ==========================================================
    # VALORIZAÇÃO SALARIAL
    # ==========================================================

    st.subheader("💹 Ocupações com Maior Valorização Salarial")

    sal_inicio = (
        df[df["ano"] == ano_inicial]
        [["ocupacao", "salario_medio"]]
        .rename(columns={"salario_medio": "salario_inicio"})
    )

    sal_fim = (
        df[df["ano"] == ano_final]
        [["ocupacao", "salario_medio"]]
        .rename(columns={"salario_medio": "salario_fim"})
    )

    valorizacao = sal_inicio.merge(
        sal_fim,
        on="ocupacao"
    )

    valorizacao = valorizacao[
        valorizacao["salario_inicio"] > 0
    ]

    valorizacao["valorizacao_%"] = (
        (valorizacao["salario_fim"] - valorizacao["salario_inicio"])
        / valorizacao["salario_inicio"]
    ) * 100

    valorizacao = valorizacao.sort_values(
        "valorizacao_%",
        ascending=False
    ).head(15)

    fig_val = px.bar(
        valorizacao,
        x="ocupacao",
        y="valorizacao_%",
        text="valorizacao_%",
        color="valorizacao_%",
        color_continuous_scale="Blues"
    )

    fig_val.update_traces(
        texttemplate="%{text:.1f}%"
    )

    fig_val.update_layout(
        height=700,
        xaxis_tickangle=-35
    )

    

    st.plotly_chart(fig_val, use_container_width=True)

    st.caption("Fonte dos dados: CBO")

except FileNotFoundError:
    st.error(
        "Arquivo 'rais_ocupacoes_limpo.csv' não encontrado em data/processed."
    )

except KeyError as e:
    st.error(
        f"Coluna obrigatória não encontrada na base: {e}"
    )

except pd.errors.EmptyDataError:
    st.error(
        "O arquivo CSV está vazio."
    )

except Exception as e:
    st.error(
        f"Erro ao processar a página: {e}"
    )
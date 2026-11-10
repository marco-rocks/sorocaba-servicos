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

ANO_MAX = 2025  # teto da série histórica (padronização entre as telas)

st.title("💼 Salários e Ocupações Formais em Sorocaba")
st.markdown(
    """
    Análise aprofundada das ocupações formais, contingente de trabalhadores, 
    remuneração média, massa salarial e dinâmica de crescimento (TGCA) com base nos microdados da RAIS.
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
    df = df[df["ano"] <= ANO_MAX]

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

    # ==========================================================
    # RANKING GERAL DE OCUPAÇÕES
    # ==========================================================

    st.markdown("---")

    st.subheader("🏅 Ranking Geral de Ocupações")

    rk = df_ano.copy()
    rk["massa_salarial"] = rk["trabalhadores"] * rk["salario_medio"]

    rk["Pos. Trabalhadores"] = rk["trabalhadores"].rank(ascending=False, method="min").astype(int)
    rk["Pos. Massa Salarial"] = rk["massa_salarial"].rank(ascending=False, method="min").astype(int)

    # Ranking salarial só entre ocupações com base mínima (evita distorção de poucos casos)
    elegiveis = rk["trabalhadores"] >= 30
    rk["Pos. Salário"] = pd.NA
    rk.loc[elegiveis, "Pos. Salário"] = (
        rk.loc[elegiveis, "salario_medio"].rank(ascending=False, method="min").astype(int)
    )
    rk["Pos. Salário"] = rk["Pos. Salário"].astype("Int64")

    # Variação de posição (ano inicial -> ano final), por nº de trabalhadores
    r_ini = df[df["ano"] == ano_inicial][["ocupacao", "trabalhadores"]].copy()
    r_fim = df[df["ano"] == ano_final][["ocupacao", "trabalhadores"]].copy()
    r_ini["pos_ini"] = r_ini["trabalhadores"].rank(ascending=False, method="min")
    r_fim["pos_fim"] = r_fim["trabalhadores"].rank(ascending=False, method="min")
    var_pos = r_ini[["ocupacao", "pos_ini"]].merge(r_fim[["ocupacao", "pos_fim"]], on="ocupacao")
    var_pos["Var. Posição"] = (var_pos["pos_ini"] - var_pos["pos_fim"]).astype(int)  # positivo = subiu
    rk = rk.merge(var_pos[["ocupacao", "Var. Posição"]], on="ocupacao", how="left")

    ordem = st.radio(
        "Ordenar ranking por",
        ["Trabalhadores", "Salário Médio", "Massa Salarial"],
        horizontal=True
    )
    campo = {"Trabalhadores": "trabalhadores", "Salário Médio": "salario_medio", "Massa Salarial": "massa_salarial"}[ordem]

    busca = st.text_input("🔎 Buscar ocupação")
    rk_view = rk.sort_values(campo, ascending=False).reset_index(drop=True)
    if busca:
        rk_view = rk_view[rk_view["ocupacao"].str.contains(busca, case=False, na=False)]

    tabela = rk_view[[
        "ocupacao", "codigo_cbo", "trabalhadores", "salario_medio", "massa_salarial",
        "Pos. Trabalhadores", "Pos. Salário", "Pos. Massa Salarial", "Var. Posição"
    ]].rename(columns={
        "ocupacao": "Ocupação", "codigo_cbo": "CBO", "trabalhadores": "Trabalhadores",
        "salario_medio": "Salário Médio", "massa_salarial": "Massa Salarial"
    })

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Trabalhadores": st.column_config.NumberColumn(format="%d"),
            "Salário Médio": st.column_config.NumberColumn(format="R$ %.2f"),
            "Massa Salarial": st.column_config.NumberColumn(format="R$ %.0f"),
            "Var. Posição": st.column_config.NumberColumn(
                format="%+d", help=f"Posições ganhas (+) ou perdidas (-) em nº de trabalhadores, {ano_inicial}→{ano_final}"
            ),
        }
    )
    st.caption("Fonte dos dados: MTE / RAIS — Microdados por CBO / Ministério do Trabalho e Emprego.")

    # ==========================================================
    # TGCA - TAXA GEOMÉTRICA DE CRESCIMENTO ANUAL DAS OCUPAÇÕES
    # ==========================================================
    st.markdown("---")
    st.header("📈 TGCA e Crescimento Acumulado por Ocupação")
    st.markdown(f"""
    A **Taxa Geométrica de Crescimento Anual (TGCA / CAGR)** mede o ritmo composto de expansão anual de cada profissão 
    entre o ano inicial ({ano_inicial}) e o ano final ({ano_final}) da série histórica:
    $$\\text{{TGCA}} = \\left( \\frac{{\\text{{Trabalhadores}}_{{\\text{{{ano_final}}}}}}}{{\\text{{Trabalhadores}}_{{\\text{{{ano_inicial}}}}}}} \\right)^{{\\frac{{1}}{{n}}}} - 1$$
    onde $n = {ano_final - ano_inicial}$ anos. Para evitar distorções de ocupações muito pequenas, o filtro considera ocupações com base mínima de vínculos formais.
    """)

    g_ano = df.groupby(["ano", "ocupacao"], as_index=False)["trabalhadores"].sum()
    df_ini = g_ano[g_ano["ano"] == ano_inicial].rename(columns={"trabalhadores": "trab_ini"})[["ocupacao", "trab_ini"]]
    df_fim = g_ano[g_ano["ano"] == ano_final].rename(columns={"trabalhadores": "trab_fim"})[["ocupacao", "trab_fim"]]
    df_tgca = df_ini.merge(df_fim, on="ocupacao")

    base_min = st.slider("Base mínima de vínculos no ano inicial (" + str(ano_inicial) + ")", min_value=100, max_value=2000, value=300, step=100)
    df_tgca_filtrado = df_tgca[df_tgca["trab_ini"] >= base_min].copy()

    n_periodo = ano_final - ano_inicial
    if n_periodo > 0 and not df_tgca_filtrado.empty:
        df_tgca_filtrado["Cresc_Acumulado_%"] = ((df_tgca_filtrado["trab_fim"] - df_tgca_filtrado["trab_ini"]) / df_tgca_filtrado["trab_ini"]) * 100
        df_tgca_filtrado["TGCA_%"] = ((df_tgca_filtrado["trab_fim"] / df_tgca_filtrado["trab_ini"]) ** (1 / n_periodo) - 1) * 100
        df_tgca_filtrado["Saldo_Vagas"] = df_tgca_filtrado["trab_fim"] - df_tgca_filtrado["trab_ini"]

        col_tg1, col_tg2 = st.columns(2)

        with col_tg1:
            st.markdown(f"##### 🚀 Top 10 Ocupações com Maior TGCA ({ano_inicial}–{ano_final})")
            top_tgca = df_tgca_filtrado.sort_values("TGCA_%", ascending=False).head(10).copy()
            top_tgca["Rotulo"] = top_tgca["TGCA_%"].apply(lambda v: f"{v:+.1f}".replace(".", ",") + "% a.a.")
            fig_tgca = px.bar(
                top_tgca, x="TGCA_%", y="ocupacao", orientation="h", text="Rotulo",
                title=f"<b>Maiores Taxas Anualizadas de Crescimento (TGCA) — Base ≥ {base_min}</b>",
                labels={"TGCA_%": "TGCA (% ao ano)", "ocupacao": "Ocupação"},
                color="TGCA_%", color_continuous_scale="Greens"
            )
            fig_tgca.update_traces(textposition="outside")
            fig_tgca.update_layout(title_font_size=14, height=480, yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
            st.plotly_chart(fig_tgca, use_container_width=True)
            st.caption("Fonte: Elaboração própria com base nos microdados da RAIS / MTE.")

        with col_tg2:
            st.markdown(f"##### 📦 Top 10 Ocupações em Crescimento Acumulado Absoluto (Saldo de Vagas)")
            top_saldo = df_tgca_filtrado.sort_values("Saldo_Vagas", ascending=False).head(10).copy()
            top_saldo["Rotulo"] = top_saldo["Saldo_Vagas"].apply(lambda v: f"{int(v):+,}".replace(",", "."))
            fig_saldo = px.bar(
                top_saldo, x="Saldo_Vagas", y="ocupacao", orientation="h", text="Rotulo",
                title=f"<b>Maior Geração Líquida Acumulada de Postos ({ano_inicial} a {ano_final})</b>",
                labels={"Saldo_Vagas": "Saldo Líquido de Trabalhadores", "ocupacao": "Ocupação"},
                color="Saldo_Vagas", color_continuous_scale="Blues"
            )
            fig_saldo.update_traces(textposition="outside")
            fig_saldo.update_layout(title_font_size=14, height=480, yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
            st.plotly_chart(fig_saldo, use_container_width=True)
            st.caption("Fonte: Elaboração própria com base nos microdados da RAIS / MTE.")

        # Tabela completa de TGCA
        with st.expander(f"📋 Ver Tabela Completa de TGCA e Variação Acumulada ({ano_inicial}–{ano_final})"):
            df_tgca_tabela = df_tgca_filtrado.sort_values("TGCA_%", ascending=False).rename(columns={
                "ocupacao": "Ocupação", "trab_ini": f"Vínculos ({ano_inicial})", "trab_fim": f"Vínculos ({ano_final})",
                "Saldo_Vagas": "Saldo Líquido", "Cresc_Acumulado_%": "Crescimento Acumulado (%)", "TGCA_%": "TGCA (% a.a.)"
            })
            st.dataframe(
                df_tgca_tabela,
                use_container_width=True,
                hide_index=True,
                column_config={
                    f"Vínculos ({ano_inicial})": st.column_config.NumberColumn(format="%d"),
                    f"Vínculos ({ano_final})": st.column_config.NumberColumn(format="%d"),
                    "Saldo Líquido": st.column_config.NumberColumn(format="%+d"),
                    "Crescimento Acumulado (%)": st.column_config.NumberColumn(format="%+.2f%%"),
                    "TGCA (% a.a.)": st.column_config.NumberColumn(format="%+.2f%%"),
                }
            )
            st.caption("Fonte: RAIS / MTE — Cálculo da Taxa Geométrica de Crescimento Anual.")

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
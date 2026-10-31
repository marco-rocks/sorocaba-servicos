import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="05 — Mobilidade Regional",
    page_icon="🚗",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw" / "mobilidade"

st.title("🚗 Mobilidade Regional")
st.markdown(
    """
    Análise da mobilidade dos trabalhadores residentes em Sorocaba,
    considerando o local de exercício do trabalho principal segundo o
    Censo Demográfico 2010 (IBGE).

    Fonte dos dados: SIDRA/IBGE
    """
)

# ==========================================================
# CARREGAMENTO
# ==========================================================

@st.cache_data
def carregar_dados():

    df = pd.read_csv(
        DATA_DIR / "mobilidade_regional_tratada.csv"
    )

    df["trabalhadores"] = pd.to_numeric(
        df["trabalhadores"],
        errors="coerce"
    )

    df = df.dropna(subset=["trabalhadores"])

    return df


try:

    df = carregar_dados()

    if df.empty:
        st.warning("Nenhum dado encontrado.")
        st.stop()

    # ==========================================================
    # KPIs
    # ==========================================================

    residencia = int(
        df.loc[
            df["local_trabalho"] == "Município de residência",
            "trabalhadores"
        ].sum()
    )

    outro_municipio = int(
        df.loc[
            df["local_trabalho"] == "Outro município",
            "trabalhadores"
        ].sum()
    )

    multiplo = int(
        df.loc[
            df["local_trabalho"] == "Mais de um município ou país",
            "trabalhadores"
        ].sum()
    )

    exterior = int(
        df.loc[
            df["local_trabalho"] == "País estrangeiro",
            "trabalhadores"
        ].sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏠 Município de Residência",
        f"{residencia:,}".replace(",", ".")
    )

    col2.metric(
        "🚗 Outro Município",
        f"{outro_municipio:,}".replace(",", ".")
    )

    col3.metric(
        "🌎 Mais de um Município",
        f"{multiplo:,}".replace(",", ".")
    )

    col4.metric(
        "✈️ País Estrangeiro",
        f"{exterior:,}".replace(",", ".")
    )

    st.markdown("---")

    # ==========================================================
    # DISTRIBUIÇÃO GERAL
    # ==========================================================

    st.subheader("📊 Distribuição dos Trabalhadores por Local de Trabalho")

    resumo = (
        df.groupby(
            "local_trabalho",
            as_index=False
        )["trabalhadores"]
        .sum()
        .sort_values("trabalhadores", ascending=False)
    )

    fig_dist = px.bar(
        resumo,
        y="local_trabalho",
        x="trabalhadores",
        orientation="h",
        text="trabalhadores",
        color="trabalhadores",
        color_continuous_scale="Blues"
    )

    fig_dist.update_layout(
        height=600,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig_dist,
        use_container_width=True
    )

    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # ==========================================================
    # PARTICIPAÇÃO %
    # ==========================================================

    st.subheader("🥧 Participação Percentual")

    fig_pizza = px.pie(
        resumo,
        values="trabalhadores",
        names="local_trabalho",
        hole=0.5
    )

    fig_pizza.update_layout(
        height=700
    )

    st.plotly_chart(
        fig_pizza,
        use_container_width=True
    )

    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # ==========================================================
    # TOP SETORES DE OUTRO MUNICÍPIO
    # ==========================================================

    st.subheader("🏭 Setores com Maior Mobilidade para Outro Município")

    df_outro = (
        df[
            df["local_trabalho"] == "Outro município"
        ]
        .sort_values(
            "trabalhadores",
            ascending=False
        )
        .head(15)
    )

    fig_outro = px.bar(
        df_outro,
        x="atividade",
        y="trabalhadores",
        text="trabalhadores",
        color="trabalhadores",
        color_continuous_scale="Reds"
    )

    fig_outro.update_layout(
        height=700,
        xaxis_tickangle=-35
    )

    st.plotly_chart(
        fig_outro,
        use_container_width=True
    )

    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # ==========================================================
    # COMPARATIVO POR ATIVIDADE
    # ==========================================================

    st.subheader(
        "⚖️ Comparativo: Município de Residência x Outro Município"
    )

    comp = df[
        df["local_trabalho"].isin(
            [
                "Município de residência",
                "Outro município"
            ]
        )
    ]

    fig_comp = px.bar(
        comp,
        x="atividade",
        y="trabalhadores",
        color="local_trabalho",
        barmode="group"
    )

    fig_comp.update_layout(
        height=750,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_comp,
        use_container_width=True
    )

    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # ==========================================================
    # TAXA DE MOBILIDADE
    # ==========================================================

    st.subheader("🔥 Taxa de Mobilidade por Setor")

    residencia_df = (
        df[
            df["local_trabalho"] == "Município de residência"
        ][["atividade", "trabalhadores"]]
        .rename(
            columns={
                "trabalhadores": "residencia"
            }
        )
    )

    outro_df = (
        df[
            df["local_trabalho"] == "Outro município"
        ][["atividade", "trabalhadores"]]
        .rename(
            columns={
                "trabalhadores": "outro"
            }
        )
    )

    taxa = pd.merge(
        residencia_df,
        outro_df,
        on="atividade",
        how="inner"
    )

    taxa["mobilidade_%"] = (
        taxa["outro"]
        /
        (taxa["residencia"] + taxa["outro"])
    ) * 100

    taxa = (
        taxa
        .sort_values(
            "mobilidade_%",
            ascending=False
        )
        .head(15)
    )

    fig_taxa = px.bar(
        taxa,
        x="atividade",
        y="mobilidade_%",
        text="mobilidade_%",
        color="mobilidade_%",
        color_continuous_scale="OrRd"
    )

    fig_taxa.update_traces(
        texttemplate="%{text:.1f}%"
    )

    fig_taxa.update_layout(
        height=750,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_taxa,
        use_container_width=True
    )

    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # ==========================================================
    # HEATMAP
    # ==========================================================

    st.subheader("🌡️ Heatmap de Mobilidade")

    heatmap = df.pivot_table(
        values="trabalhadores",
        index="atividade",
        columns="local_trabalho",
        aggfunc="sum",
        fill_value=0
    )

    fig_heat = px.imshow(
        heatmap,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="YlOrRd"
    )

    fig_heat.update_layout(
        height=900
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

    st.caption("Fonte dos dados: SIDRA/IBGE")

    st.markdown("---")

    # ==========================================================
    # TABELA
    # ==========================================================

    st.subheader("📋 Base Completa")

    st.dataframe(
        df.sort_values(
            "trabalhadores",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.caption("Fonte dos dados: SIDRA/IBGE")

    # ==========================================================
    # LOCOMOÇÃO INDUSTRIAL
    # ==========================================================

    st.markdown("---")
    st.header("🏭 Locomoção Industrial")

    palavras_ind = ("indústria", "industria", "transformação", "transformacao", "extrativ")
    atividades = sorted(df["atividade"].dropna().unique())
    padrao_ind = [a for a in atividades if any(p in a.lower() for p in palavras_ind)]

    ativ_sel = st.multiselect(
        "Atividades consideradas industriais",
        atividades,
        default=padrao_ind
    )

    if not ativ_sel:
        st.info("Selecione ao menos uma atividade para ver a análise industrial.")
    else:
        df_ind = df[df["atividade"].isin(ativ_sel)]

        ind_res = int(df_ind.loc[df_ind["local_trabalho"] == "Município de residência", "trabalhadores"].sum())
        ind_out = int(df_ind.loc[df_ind["local_trabalho"] == "Outro município", "trabalhadores"].sum())
        taxa_ind = (ind_out / (ind_res + ind_out) * 100) if (ind_res + ind_out) > 0 else 0

        taxa_geral_base = (
            df.loc[df["local_trabalho"] == "Município de residência", "trabalhadores"].sum()
            + df.loc[df["local_trabalho"] == "Outro município", "trabalhadores"].sum()
        )
        taxa_geral = (outro_municipio / taxa_geral_base * 100) if taxa_geral_base > 0 else 0

        i1, i2, i3 = st.columns(3)
        i1.metric("🏭 Industriais que trabalham em outro município", f"{ind_out:,}".replace(",", "."))
        i2.metric("Taxa de locomoção industrial", f"{taxa_ind:.1f}%")
        i3.metric("Taxa geral (todos os setores)", f"{taxa_geral:.1f}%", delta=f"{taxa_ind - taxa_geral:+.1f} p.p. (indústria vs geral)")

        fig_ind = px.bar(
            df_ind[df_ind["local_trabalho"].isin(["Município de residência", "Outro município"])],
            x="atividade", y="trabalhadores", color="local_trabalho", barmode="group",
            title="Atividades industriais: trabalham na cidade vs. em outro município"
        )
        fig_ind.update_layout(height=600, xaxis_tickangle=-35)
        st.plotly_chart(fig_ind, use_container_width=True)
        st.caption("Fonte dos dados: SIDRA/IBGE (Censo 2010)")

    # --- QUAL CIDADE? (depende de base com destino) ---
    st.subheader("📍 Para qual cidade vai a locomoção industrial?")

    arq_cidades = DATA_DIR / "deslocamento_cidades.csv"
    if arq_cidades.exists():
        df_cid = pd.read_csv(arq_cidades)
        # Esperado: colunas 'cidade_destino' e 'trabalhadores' (opcional: 'atividade')
        df_cid["trabalhadores"] = pd.to_numeric(df_cid["trabalhadores"], errors="coerce")
        df_cid = df_cid.dropna(subset=["trabalhadores"])
        if "atividade" in df_cid.columns and ativ_sel:
            df_cid = df_cid[df_cid["atividade"].isin(ativ_sel)]
        rank_cid = (
            df_cid.groupby("cidade_destino", as_index=False)["trabalhadores"].sum()
            .sort_values("trabalhadores", ascending=False).head(15)
        )
        fig_cid = px.bar(
            rank_cid, x="trabalhadores", y="cidade_destino", orientation="h",
            text="trabalhadores", color="trabalhadores", color_continuous_scale="Reds",
            title="Top 15 cidades de destino"
        )
        fig_cid.update_layout(height=600, yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig_cid, use_container_width=True)
    else:
        st.info(
            "A base atual informa **quantos** trabalhadores saem de Sorocaba, mas não **para onde**. "
            "Para ver o ranking de cidades, adicione `deslocamento_cidades.csv` em `data/raw/mobilidade/` "
            "com as colunas `cidade_destino` e `trabalhadores` (opcional: `atividade`)."
        )

except FileNotFoundError:
    st.error(
        "Arquivo 'mobilidade_regional_tratada.csv' não encontrado."
    )

except KeyError as e:
    st.error(
        f"Coluna obrigatória não encontrada: {e}"
    )

except Exception as e:
    st.error(
        f"Erro ao processar a página: {e}"
    )
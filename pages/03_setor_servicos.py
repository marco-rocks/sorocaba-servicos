import re
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
ANO_MAX = 2025  # teto da série histórica (padronização entre as telas)

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

    # --- TETO DE ANO ---
    df_pess = df_pess[pd.to_numeric(df_pess["ano"], errors="coerce") <= ANO_MAX]
    df_novos = df_novos[pd.to_numeric(df_novos["Ano"], errors="coerce") <= ANO_MAX]
    df_tot = df_tot[pd.to_numeric(df_tot["Ano"], errors="coerce") <= ANO_MAX]

    return df_unid, df_pess, df_novos, df_tot

@st.cache_data
def carregar_novos_raw():
    return pd.read_csv(DATA_DIR / "novos_negocios.csv", sep=";")

def classificar_porte(valor):
    s = str(valor).lower().strip()
    if re.search(r"\bmei\b", s) or "microempreendedor" in s:
        return "MEI"
    if "microempresa" in s or "micro empresa" in s or s in ("me", "micro"):
        return "Microempresa"
    if "pequeno" in s or re.search(r"\bepp\b", s):
        return "Empresa de Pequeno Porte"
    return "Demais"

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

    # --- COMO CRESCERAM MEI E MICROEMPRESAS ---
    st.markdown("---")
    st.header("🌱 Como Cresceram MEI e Microempresas")

    df_raw = carregar_novos_raw()
    palavras = ("porte", "natureza", "categoria", "enquadramento", "tipo", "regime")
    cols_cat = [c for c in df_raw.columns if any(p in c.lower() for p in palavras)]

    if not cols_cat:
        st.warning(
            "Não encontrei em `novos_negocios.csv` uma coluna de porte/natureza jurídica. "
            f"Colunas disponíveis: {list(df_raw.columns)}"
        )
    else:
        col_porte = st.selectbox("Coluna usada para classificar o porte", cols_cat)

        df_p = df_raw.copy()
        df_p["ano"] = pd.to_numeric(df_p["ano"], errors="coerce")
        df_p["qtd_empresa"] = pd.to_numeric(df_p["qtd_empresa"], errors="coerce")
        df_p = df_p.dropna(subset=["ano", "qtd_empresa"])
        df_p = df_p[(df_p["ano"] >= ANO_INICIO_NEGOCIOS) & (df_p["ano"] <= ANO_MAX)]
        df_p["ano"] = df_p["ano"].astype(int)
        df_p["Categoria"] = df_p[col_porte].apply(classificar_porte)

        por_cat = df_p.groupby(["ano", "Categoria"], as_index=False)["qtd_empresa"].sum()
        pivot = por_cat.pivot(index="ano", columns="Categoria", values="qtd_empresa").fillna(0)

        foco = [c for c in ["MEI", "Microempresa"] if c in pivot.columns]

        if not foco:
            st.warning(
                f"Nenhum valor da coluna `{col_porte}` foi reconhecido como MEI ou Microempresa. "
                f"Valores encontrados: {sorted(df_p[col_porte].astype(str).unique())[:20]}"
            )
        else:
            ano_min, ano_max = int(pivot.index.min()), int(pivot.index.max())
            # com o teto em ANO_MAX, esse ano já é completo; sem teto atingido, o último pode estar incompleto
            ano_comp = ano_max if ano_max >= ANO_MAX else ano_max - 1

            cols_m = st.columns(len(foco))
            for i, cat in enumerate(foco):
                base = pivot.loc[ano_min, cat]
                atual = pivot.loc[ano_comp, cat]
                delta = f"{((atual - base) / base) * 100:+.1f}% vs {ano_min}" if base > 0 else f"Sem registros em {ano_min}"
                cols_m[i].metric(f"{cat}: aberturas em {ano_comp}", f"{int(atual):,}".replace(",", "."), delta=delta)

            df_lin = por_cat[por_cat["Categoria"].isin(foco)]
            fig_porte = px.line(
                df_lin, x="ano", y="qtd_empresa", color="Categoria", markers=True,
                title="Aberturas por ano: MEI e Microempresas",
                labels={"qtd_empresa": "Qtd. de Empresas", "ano": "Ano"}
            )
            fig_porte.update_layout(xaxis=dict(tickmode="linear", dtick=1), height=500, hovermode="x unified")
            st.plotly_chart(fig_porte, use_container_width=True)

            acum = pivot[foco].cumsum().reset_index().melt(id_vars="ano", var_name="Categoria", value_name="Acumulado")
            fig_acum = px.area(
                acum, x="ano", y="Acumulado", color="Categoria",
                title="Acumulado de aberturas (empresas hoje ativas)",
                labels={"Acumulado": "Qtd. acumulada", "ano": "Ano"}
            )
            fig_acum.update_layout(xaxis=dict(tickmode="linear", dtick=1), height=500)
            st.plotly_chart(fig_acum, use_container_width=True)

            fig_share = px.bar(
                por_cat, x="ano", y="qtd_empresa", color="Categoria",
                title="Participação de cada porte nas aberturas (%)",
                labels={"qtd_empresa": "% das aberturas", "ano": "Ano"}
            )
            fig_share.update_layout(barnorm="percent", xaxis=dict(tickmode="linear", dtick=1), height=500)
            st.plotly_chart(fig_share, use_container_width=True)

            st.caption(
                "Atenção: a base conta apenas negócios **hoje ativos**, por ano de abertura. Negócios abertos e "
                "encerrados no passado não aparecem, então os anos antigos tendem a ser subestimados. "
                "O MEI só existe desde 2009, e o último ano pode estar incompleto."
            )

except Exception as e:
    st.error(f"Erro ao processar a página: {e}")
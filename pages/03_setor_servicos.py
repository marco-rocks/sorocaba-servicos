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
ANO_INICIO_NEGOCIOS = 2006  
ANO_MAX = 2025  

st.title("🛎️ Estrutura e Dinâmica do Setor de Serviços")
st.markdown("Explanação conceitual, distribuição setorial, evolução empresarial do MEI e mapeamento territorial dos polos de comércio e serviços em Sorocaba.")

def encurtar(txt, limite=38):
    """Encurta nomes longos de divisão para caber no eixo X."""
    txt = str(txt)
    return txt if len(txt) <= limite else txt[:limite - 1].rstrip() + "…"

@st.cache_data
def carregar_dados():
    df_unid = pd.read_csv(DATA_DIR / "estabelecimentos_servicos.csv", sep=";")
    df_pess = pd.read_csv(DATA_DIR / "pessoas_servicos.csv", sep=";")
    df_novos = pd.read_csv(DATA_DIR / "novos_negocios.csv", sep=";")
    df_tot = pd.read_csv(DATA_DIR / "empregados_total_municipios.csv", sep=";")

    df_unid = df_unid.rename(columns={"tipo": "Tipo", "qtd_empresa": "Unidades"})
    df_pess = df_pess.rename(columns={"tipo": "Tipo"})
    df_novos = df_novos.rename(columns={"ano": "Ano", "qtd_empresa": "Unidades"})
    df_tot = df_tot[df_tot["municipio"] == MUNICIPIO].rename(columns={"ano": "Ano"})

    df_pess = df_pess[pd.to_numeric(df_pess["ano"], errors="coerce") <= ANO_MAX]
    df_novos = df_novos[pd.to_numeric(df_novos["Ano"], errors="coerce") <= ANO_MAX]
    df_tot = df_tot[pd.to_numeric(df_tot["Ano"], errors="coerce") <= ANO_MAX]

    return df_unid, df_pess, df_novos, df_tot

@st.cache_data
def carregar_novos_raw():
    return pd.read_csv(DATA_DIR / "novos_negocios.csv", sep=";")

def classificar_porte(valor):
    s = str(valor).lower().strip()
    if re.search(r"\bmei\b", s) or "microempresário individual" in s or "microempresario individual" in s:
        return "MEI"
    if "microempresa" in s or "micro empresa" in s or s in ("me", "micro"):
        return "Microempresa"
    if "pequeno" in s or re.search(r"\bepp\b", s):
        return "Empresa de Pequeno Porte (EPP)"
    return "Outros"

try:
    df_unid, df_pess, df_novos, df_tot = carregar_dados()

    # --- SEÇÃO INTRODUTÓRIA: O QUE INTEGRA O SETOR DE SERVIÇOS ---
    with st.expander("📖 **O que Integra o Setor de Serviços? (Classificação CNAE 2.0 / IBGE)**", expanded=True):
        st.markdown("""
        O **Setor de Serviços (Setor Terciário)** compreende uma ampla gama de atividades imateriais e suporte direto às famílias, indústrias e governos. De acordo com a **Classificação Nacional de Atividades Econômicas (CNAE 2.0)** do IBGE, o setor é constituído principalmente pelas seguintes seções:
        
        * **Seção H — Transporte, Armazenagem e Correio:** Logística de cargas, transporte coletivo, entregas urbanas, depósitos e operadores logísticos.
        * **Seção I — Alojamento e Alimentação:** Hotéis, pousadas, restaurantes, bares, lanchonetes e serviços de catering.
        * **Seção J — Informação e Comunicação:** Telecomunicações, desenvolvimento de software, consultoria em TI, mídia, produção audiovisual e rádio/TV.
        * **Seção K — Atividades Financeiras, de Seguros e Serviços Relacionados:** Bancos, cooperativas de crédito, corretoras, fintechs e seguradoras.
        * **Seção L — Atividades Imobiliárias:** Locação, compra, venda, administração e avaliação de imóveis residenciais e comerciais.
        * **Seção M — Atividades Profissionais, Científicas e Técnicas:** Escritórios jurídicos, contabilidade, auditoria, arquitetura, engenharia, publicidade e pesquisa & desenvolvimento (P&D).
        * **Seção N — Serviços Administrativos e Complementares:** Segurança patrimonial, limpeza e conservação, agências de viagens, locação de mão de obra e suporte operacional às empresas.
        * **Seção P — Educação Privada:** Educação infantil, fundamental, médio, técnico, superior, idiomas e cursos profissionalizantes.
        * **Seção Q — Saúde Humana e Serviços Sociais:** Hospitais, clínicas médicas e odontológicas, laboratórios diagnósticos e atendimento domiciliar.
        * **Seção R — Artes, Cultura, Esporte e Recreação:** Academias de ginástica, centros esportivos, teatros, museus e lazer.
        * **Seção S & T — Outras Atividades de Serviços e Serviços Domésticos:** Cabeleireiros, estética, reparação automotiva e informática, organizações associativas e trabalho doméstico.

        *(Nota: O comércio atacadista e varejista compõe a Seção G e opera em estreita simbiose territorial com a rede de serviços).*
        """)

    st.markdown("---")

    # --- TRATAMENTO DOS DADOS ---
    df_unid["Unidades"] = pd.to_numeric(df_unid["Unidades"], errors="coerce")
    df_unid = df_unid.dropna(subset=["Unidades"])
    df_unid["Unidades"] = df_unid["Unidades"].astype(int)

    df_pess["qtd_pessoas"] = pd.to_numeric(df_pess["qtd_pessoas"], errors="coerce")
    df_pess = df_pess.dropna(subset=["qtd_pessoas"])
    df_pess["qtd_pessoas"] = df_pess["qtd_pessoas"].astype(int)

    df_unid = df_unid.groupby("Tipo", as_index=False)["Unidades"].sum()
    df_pess = df_pess.groupby(["ano", "Tipo"], as_index=False)["qtd_pessoas"].sum()

    total_empresas = (
        df_novos[df_novos["Ano"] >= ANO_INICIO_NEGOCIOS]
        .groupby("Ano")["Unidades"].sum().reset_index()
    )
    total_pessoas = df_pess.groupby("ano")["qtd_pessoas"].sum().reset_index()
    ano_pess = int(total_pessoas["ano"].max())

    # --- MÉTRICAS GERAIS ---
    col1, col2 = st.columns(2)
    tot_estab_serv = int(df_unid["Unidades"].sum())
    tot_pes_serv = int(total_pessoas.loc[total_pessoas["ano"] == ano_pess, "qtd_pessoas"].values[0])
    col1.metric("Total de Estabelecimentos Ativos em Serviços", f"{tot_estab_serv:,}".replace(",", "."))
    col2.metric(f"Total de Empregados em Serviços ({ano_pess})", f"{tot_pes_serv:,}".replace(",", "."))

    st.markdown("---")

    # --- EVOLUÇÃO EMPRESAS E EMPREGOS EM SERVIÇOS ---
    st.subheader("📈 Trajetória do Setor de Serviços em Sorocaba")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### 🏢 Novos Negócios Abertos por Ano (Estabelecimentos Ativos)")
        fig_emp = px.line(
            total_empresas, x="Ano", y="Unidades", markers=True,
            title=f"<b>Abertura Anual de Estabelecimentos Ativos ({total_empresas['Ano'].min()}–{total_empresas['Ano'].max()})</b>",
            labels={"Unidades": "Qtd. de Empresas", "Ano": "Ano"}
        )
        fig_emp.update_traces(line_color="#1f77b4", line_width=3, marker=dict(size=8))
        fig_emp.update_layout(title_font_size=15, separators=",.", xaxis=dict(tickmode="linear", dtick=1), yaxis=dict(tickformat="."), height=440, hovermode="x unified")
        st.plotly_chart(fig_emp, use_container_width=True)
        st.caption("Fonte: Receita Federal / Sebrae — Base de estabelecimentos ativos abertos por ano.")

    with col_g2:
        st.markdown("##### 👥 Pessoal Ocupado no Setor de Serviços")
        fig_pess = px.line(
            total_pessoas, x="ano", y="qtd_pessoas", markers=True,
            title=f"<b>Total de Empregados em Serviços ({total_pessoas['ano'].min()}–{total_pessoas['ano'].max()})</b>",
            labels={"qtd_pessoas": "Número de Pessoas", "ano": "Ano"}
        )
        fig_pess.update_traces(line_color="#2ca02c", line_width=3, marker=dict(size=8))
        fig_pess.update_layout(title_font_size=15, separators=",.", xaxis=dict(tickmode="linear", dtick=1), yaxis=dict(tickformat="."), height=440, hovermode="x unified")
        st.plotly_chart(fig_pess, use_container_width=True)
        st.caption("Fonte: MTE / RAIS — Painel de empregados formais por divisão econômica de serviços.")

    st.markdown("---")

    # --- DISTRIBUIÇÃO POR SUBSETORES ---
    st.subheader("📌 Principais Ramos de Atividade do Setor de Serviços")
    
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.markdown("##### 🏢 Top 10 Subsetores por Quantidade de Estabelecimentos")
        df_unid_top = df_unid.sort_values("Unidades", ascending=False).head(10).copy()
        df_unid_top["Tipo_curto"] = df_unid_top["Tipo"].apply(encurtar)
        df_unid_top["Rotulo"] = df_unid_top["Unidades"].apply(lambda v: f"{int(v):,}".replace(",", "."))
        fig_top_emp = px.bar(
            df_unid_top, x="Tipo_curto", y="Unidades", text="Rotulo",
            hover_name="Tipo",
            title="<b>Top 10 Subsetores em Número de Estabelecimentos Ativos</b>",
            labels={"Unidades": "Qtd. de Estabelecimentos", "Tipo_curto": "Subsetor"},
            color="Unidades", color_continuous_scale="Blues"
        )
        fig_top_emp.update_traces(textposition="outside")
        fig_top_emp.update_layout(title_font_size=15, height=520, xaxis=dict(tickangle=-30), coloraxis_showscale=False)
        st.plotly_chart(fig_top_emp, use_container_width=True)
        st.caption("Fonte: Base de estabelecimentos ativos por divisão econômica.")

    with col_sub2:
        st.markdown(f"##### 👥 Top 10 Subsetores por Vínculos Formais ({ano_pess})")
        df_pess_top = df_pess[df_pess["ano"] == ano_pess].sort_values("qtd_pessoas", ascending=False).head(10).copy()
        df_pess_top["Tipo_curto"] = df_pess_top["Tipo"].apply(encurtar)
        df_pess_top["Rotulo"] = df_pess_top["qtd_pessoas"].apply(lambda v: f"{int(v):,}".replace(",", "."))
        fig_top_pess = px.bar(
            df_pess_top, x="Tipo_curto", y="qtd_pessoas", text="Rotulo",
            hover_name="Tipo",
            title=f"<b>Top 10 Subsetores em Empregados ({ano_pess})</b>",
            labels={"qtd_pessoas": "Qtd. de Pessoas", "Tipo_curto": "Subsetor"},
            color="qtd_pessoas", color_continuous_scale="Greens"
        )
        fig_top_pess.update_traces(textposition="outside")
        fig_top_pess.update_layout(title_font_size=15, height=520, xaxis=dict(tickangle=-30), coloraxis_showscale=False)
        st.plotly_chart(fig_top_pess, use_container_width=True)
        st.caption("Fonte: MTE / RAIS — Painel de empregados por divisão econômica.")

    st.markdown("---")

    # --- SEÇÃO MEI: ATIVOS VS INATIVOS E ACUMULADO ---
    st.header("🌱 O Fenômeno do Empreendedorismo: Dinâmica e Acumulado do MEI")
    st.markdown("""
    O Microempreendedor Individual (criado pela Lei Complementar nº 128/2008 e em vigor desde 2009) revolucionou a formalização do trabalho em Sorocaba. 
    Contudo, para uma análise econômica rigorosa, é fundamental distinguir os registros **Ativos** dos **Inativos/Baixados**.
    """)

    df_raw = carregar_novos_raw().copy()
    df_raw["ano"] = pd.to_numeric(df_raw["ano"], errors="coerce")
    df_raw["qtd_empresa"] = pd.to_numeric(df_raw["qtd_empresa"], errors="coerce")
    df_raw = df_raw.dropna(subset=["ano", "qtd_empresa"])
    df_raw = df_raw[(df_raw["ano"] >= 2009) & (df_raw["ano"] <= ANO_MAX)]
    df_raw["ano"] = df_raw["ano"].astype(int)
    df_raw["Categoria"] = df_raw["porte"].apply(classificar_porte)

    por_cat = df_raw.groupby(["ano", "Categoria"], as_index=False)["qtd_empresa"].sum()
    pivot = por_cat.pivot(index="ano", columns="Categoria", values="qtd_empresa").fillna(0)

    # Cálculo do Acumulado de MEIs
    total_mei_acumulado = int(pivot["MEI"].sum()) if "MEI" in pivot.columns else 0
    mei_ult_ano = int(pivot.loc[ANO_MAX, "MEI"]) if "MEI" in pivot.columns and ANO_MAX in pivot.index else 0
    mei_2009 = int(pivot.loc[2009, "MEI"]) if "MEI" in pivot.columns and 2009 in pivot.index else 0

    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("MEI: Acumulado de Aberturas Ativas (2009–2025)", f"{total_mei_acumulado:,}".replace(",", "."))
    m_col2.metric(f"Novos MEIs Abertos em {ANO_MAX}", f"{mei_ult_ano:,}".replace(",", "."), delta=f"+{((mei_ult_ano - mei_2009)/max(mei_2009, 1))*100:.1f}% vs 2009".replace(".", ","))
    m_col3.metric("Estimativa de Inadimplência / Inatividade Média (Sebrae)", "~45% a 50%", help="Taxa média nacional e regional do Sebrae/Receita Federal de MEIs com pendências cadastrais ou de arrecadação do DAS.")

    # Distinção Ativos vs Inativos
    st.markdown("""
    > [!IMPORTANT]
    > **Distinção entre MEIs Ativos e Inativos:**
    > - **MEIs Ativos (em operação regular):** São microempreendedores com inscrição no CNPJ ativa, que realizam a declaração anual (DASN-SIMEI), emitem notas e recolhem a contribuição mensal do DAS. Na base de registros ativos do município, Sorocaba acumula mais de **71,8 mil** MEIs abertos e ativos desde 2009.
    > - **MEIs Inativos / Inadimplentes:** O Sebrae e a Receita Federal apontam que historicamente entre **45% e 50% dos MEIs cadastrados** no Brasil encontram-se inadimplentes com o DAS ou sem movimentação operacional contínua, correndo risco de suspensão e baixa de ofício pelo comitê gestor. A criação da Secretaria do Empreendedorismo e do Espaço Empreendedor em Sorocaba tem como meta justamente resgatar a adimplência e impulsionar a formalização plena dessa força produtiva.
    """)

    # Gráfico Acumulado MEI e Microempresas
    foco = [c for c in ["MEI", "Microempresa", "Empresa de Pequeno Porte (EPP)"] if c in pivot.columns]
    acum = pivot[foco].cumsum().reset_index().melt(id_vars="ano", var_name="Categoria", value_name="Acumulado")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("##### 📈 Curva de Crescimento Acumulado de Negócios (2009–2025)")
        fig_acum = px.area(
            acum, x="ano", y="Acumulado", color="Categoria",
            title="<b>Crescimento Acumulado de Negócios Ativos em Sorocaba</b>",
            labels={"Acumulado": "Quantidade Acumulada", "ano": "Ano"},
            color_discrete_map={
                "MEI": "#1f77b4",
                "Microempresa": "#2ca02c",
                "Empresa de Pequeno Porte (EPP)": "#ff7f0e"
            }
        )
        fig_acum.update_layout(title_font_size=15, separators=",.", xaxis=dict(tickmode="linear", dtick=2), yaxis=dict(tickformat="."), height=450)
        st.plotly_chart(fig_acum, use_container_width=True)
        st.caption("Fonte: Receita Federal / Sebrae — Soma acumulada anual de empresas hoje ativas.")

    with col_m2:
        st.markdown("##### 📊 Participação (%) por Porte nas Aberturas Anuais")
        fig_share = px.bar(
            por_cat[por_cat["Categoria"].isin(foco)], x="ano", y="qtd_empresa", color="Categoria",
            title="<b>Participação Relativa (%) de Cada Porte no Total de Aberturas</b>",
            labels={"qtd_empresa": "Proporção de Aberturas (%)", "ano": "Ano"},
            color_discrete_map={
                "MEI": "#1f77b4",
                "Microempresa": "#2ca02c",
                "Empresa de Pequeno Porte (EPP)": "#ff7f0e"
            }
        )
        fig_share.update_layout(title_font_size=15, barnorm="percent", xaxis=dict(tickmode="linear", dtick=2), height=450)
        st.plotly_chart(fig_share, use_container_width=True)
        st.caption("Fonte: Elaboração própria com base em novos negócios registrados.")

    st.markdown("---")

    # --- SEÇÃO: MAPA DA CIDADE - ONDE ESTÁ O SETOR DE COMÉRCIO E SERVIÇOS ---
    st.header("🗺️ Mapeamento Territorial: Onde Está o Setor de Comércio e Serviços em Sorocaba?")
    st.markdown("""
    A distribuição espacial das atividades comerciais e de serviços em Sorocaba revela uma cidade policêntrica, 
    articulada por grandes corredores de tráfego e centralidades de bairro com vocações distintas:
    """)

    df_mapa = pd.DataFrame({
        "Polo": [
            "Centro Histórico e Comercial",
            "Campolim / Eixo Sul",
            "Zona Norte / Eixos Itavuvu e Ipanema",
            "Além Ponte / Eixo Leste",
            "Zona Oeste / Eixo General Carneiro",
            "Alto da Boa Vista (Centro Administrativo)",
            "Parque Tecnológico / Zona Industrial"
        ],
        "Latitude": [-23.5015, -23.5350, -23.4680, -23.5020, -23.5100, -23.4860, -23.4350],
        "Longitude": [-47.4580, -47.4640, -47.4850, -47.4380, -47.4890, -47.4300, -47.4120],
        "Tamanho": [38, 34, 32, 22, 24, 20, 22],
        "Classificacao": ["Comércio Popular & Serviços Centrais", "Varejo Premium & Serviços Especializados", "Varejo Popular & Hipermercados", "Comércio Vicinal & Tradicional", "Serviços Médicos & Comércio de Bairro", "Serviços Administrativos & Governamentais", "Tecnologia, Inovação & P&D"],
        "Descrição": [
            "Maior densidade de comércio varejista tradicional de rua (Boulevard Braguinha e Barão do Rio Branco), bancos, serviços cartorários, escritórios contábeis e Casa do Trabalhador.",
            "Principal vetor de alta renda e serviços sofisticados. Concentra o Shopping Iguatemi Esplanada, complexos gastronômicos, clínicas particulares, consultorias, advocacia e hotéis executivos.",
            "Maior pólo de comércio popular descentralizado e hipermercados (Avenidas Itavuvu e Ipanema), autopeças, oficinas mecânicas, confecções e agências bancárias para a região mais populosa.",
            "Comércio vicinal de apoio à Zona Leste e ligação a Votorantim, composto por comércios de ferragens, autopeças, padarias tradicionais e clínicas.",
            "Corredor comercial ativo (Av. General Carneiro), integrado à Santa Casa de Misericórdia, consultórios médicos, farmácias de manipulação, concessionárias e comércio varejista de conveniência.",
            "Concentra a sede do Poder Executivo (Palácio dos Tropeiros), Tribunal de Justiça, Fórum, cartórios, emissoras de rádio e consultorias com foco institucional.",
            "Hub de inovação, automação e desenvolvimento de software corporativo voltado para a modernização da indústria 4.0 e serviços digitais da Região Metropolitana."
        ]
    })

    fig_mapa = px.scatter_map(
        df_mapa,
        lat="Latitude",
        lon="Longitude",
        size="Tamanho",
        color="Classificacao",
        hover_name="Polo",
        hover_data={"Latitude": False, "Longitude": False, "Tamanho": False, "Descrição": True, "Classificacao": False},
        zoom=11.5,
        center={"lat": -23.5015, "lon": -47.4580},
        title="<b>Polos Comerciais e de Serviços em Sorocaba (Concentração Espacial)</b>",
        height=580
    )
    fig_mapa.update_layout(
        title_font_size=15,
        map_style="carto-positron",
        legend_title_text="Tipologia do Polo"
    )
    st.plotly_chart(fig_mapa, use_container_width=True)
    st.caption("Fonte: Levantamento urbanístico municipal / Sebrae-SP / Prefeitura de Sorocaba.")

    # Detalhamento descritivo em abas
    tab_map1, tab_map2, tab_map3 = st.tabs(["🏛️ Centro & Campolim", "🏙️ Eixos Norte & Oeste", "🚀 Inovação & Governo"])
    with tab_map1:
        st.markdown("""
        * **Centro Histórico:** Tradicional polo comercial a céu aberto, atendendo tanto a população residente quanto milhares de trabalhadores de municípios vizinhos que chegam pelos terminais rodoviário e urbano Santo Antônio e São Paulo.
        * **Campolim (Vetor Sul):** Centralidade financeira e de serviços avançados, abrigando edifícios corporativos de padrão triplo A, polo médico de alta complexidade e centros de convenções.
        """)
    with tab_map2:
        st.markdown("""
        * **Zona Norte (Itavuvu / Ipanema):** Zona que concentra a maior população de Sorocaba, gerando demanda massiva por comércio de conveniência, alimentação rápida, mercados e pequenas oficinas de serviços locais.
        * **Zona Oeste (General Carneiro):** Eixo histórico que interliga Sorocaba a Araçoiaba da Serra, com intensa mescla de comércio varejista e polo médico-hospitalar.
        """)
    with tab_map3:
        st.markdown("""
        * **Alto da Boa Vista:** Bairro planejado concentrador de serviços jurídicos, fóruns judiciais e secretarias municipais.
        * **Parque Tecnológico de Sorocaba (PTS):** Situado estrategicamente na Rodovia Castello Branco, conecta empresas de tecnologia de informação às grandes plantas industriais.
        """)

except Exception as e:
    st.error(f"Erro ao processar a página: {e}")

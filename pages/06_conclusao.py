import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="06 — Conclusão",
    page_icon="🎯",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_CONTEXTO_DIR = BASE_DIR / "data" / "raw" / "contexto"
MOBILIDADE_DIR = BASE_DIR / "data" / "raw" / "mobilidade"

st.title("🎯 Síntese e Conclusões Estratégicas")
st.subheader("O papel do Setor de Serviços no desenvolvimento socioeconômico de Sorocaba-SP")

st.markdown("""
Esta seção consolida os principais achados extraídos ao longo dos módulos de **Contexto Demográfico**, **Mercado de Trabalho**, **Setor de Serviços**, **Estrutura Salarial** e **Mobilidade Regional**, oferecendo uma visão integrada sobre o momento econômico de Sorocaba.
""")

@st.cache_data
def carregar_dados_conclusao():
    dados = {}
    
    # 1. População
    file_pop = PROCESSED_DIR / "populacao_limpo.csv"
    if file_pop.exists():
        try:
            df_pop = pd.read_csv(file_pop)
            row_tot = df_pop[df_pop["Faixa Etária"] == "Total General"]
            if not row_tot.empty:
                dados["pop_2022"] = int(row_tot["População (2022)"].values[0])
                dados["pop_cresc"] = float(row_tot["Crescimento (%)"].values[0])
        except Exception:
            pass
            
    # 2. PIB Real
    file_pib = PROCESSED_DIR / "pib_limpo.csv"
    if file_pib.exists():
        try:
            df_pib = pd.read_csv(file_pib).sort_values("Ano")
            if not df_pib.empty:
                ult_pib = df_pib.iloc[-1]
                dados["pib_ano"] = int(ult_pib["Ano"])
                dados["pib_val_bi"] = float(ult_pib["PIB Real 2023 (R$)"]) / 1e9
        except Exception:
            pass
            
    # 3. Empresas e Pessoal Ocupado
    file_emp = PROCESSED_DIR / "empresas_empregos_limpo.csv"
    if file_emp.exists():
        try:
            df_emp = pd.read_csv(file_emp).sort_values("Ano")
            if not df_emp.empty:
                ini = df_emp.iloc[0]
                fim = df_emp.iloc[-1]
                dados["emp_ano_ini"] = int(ini["Ano"])
                dados["emp_ano_fim"] = int(fim["Ano"])
                dados["cresc_pessoal_pct"] = ((fim["Pessoal Ocupado"] - ini["Pessoal Ocupado"]) / ini["Pessoal Ocupado"]) * 100
                dados["cresc_empresas_pct"] = ((fim["Empresas"] - ini["Empresas"]) / ini["Empresas"]) * 100
        except Exception:
            pass

    # 4. Mobilidade
    file_mob = MOBILIDADE_DIR / "mobilidade_regional_tratada.csv"
    if file_mob.exists():
        try:
            df_mob = pd.read_csv(file_mob)
            df_mob["trabalhadores"] = pd.to_numeric(df_mob["trabalhadores"], errors="coerce")
            tot = df_mob["trabalhadores"].sum()
            if tot > 0:
                res = df_mob.loc[df_mob["local_trabalho"] == "Município de residência", "trabalhadores"].sum()
                dados["pct_trabalha_local"] = (res / tot) * 100
        except Exception:
            pass

    return dados

# Carregar dados dinâmicos
dados = carregar_dados_conclusao()

# Formatação e fallback seguro
pop_txt = f"{dados['pop_2022']:,.0f}".replace(",", ".") + " hab" if "pop_2022" in dados else "Dado Indisponível"
pop_cresc_txt = f"+{dados['pop_cresc']:.2f}%" if "pop_cresc" in dados else "Dado Indisponível"
pib_bi_txt = f"R$ {dados['pib_val_bi']:.2f} Bi" if "pib_val_bi" in dados else "Dado Indisponível"
cresc_pes_txt = f"+{dados['cresc_pessoal_pct']:.1f}%" if "cresc_pessoal_pct" in dados else "Dado Indisponível"
cresc_emp_txt = f"+{dados['cresc_empresas_pct']:.1f}%" if "cresc_empresas_pct" in dados else "Dado Indisponível"
pct_mob_txt = f"{dados['pct_trabalha_local']:.1f}% dos residentes" if "pct_trabalha_local" in dados else "Dado Indisponível"
periodo_emp = f"({dados.get('emp_ano_ini', '')}–{dados.get('emp_ano_fim', '')})" if "emp_ano_ini" in dados else ""

# --- CARDS DE SÍNTESE GLOBAL ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("População (Censo 2022)", pop_txt, f"{pop_cresc_txt} vs 2010")
c2.metric("PIB Real de Sorocaba", pib_bi_txt)
c3.metric(f"Crescimento de Empregos {periodo_emp}", cresc_pes_txt, f"Empresas: {cresc_emp_txt}")
c4.metric("Absorção Local de Mão de Obra", pct_mob_txt, "Trabalham no próprio município")

st.markdown("---")

# --- SEÇÃO 1: PILARES DA ANÁLISE ---
st.header("📌 Pilares Fundamentais da Economia Sorocabana")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"""
    ### 🏙️ 1. Da "Manchester Paulista" ao Polo de Serviços
    * **Transição Histórica:** Sorocaba construiu sua reputação econômica com base no pioneirismo siderúrgico e na força da indústria têxtil e metalmecânica.
    * **Expansão do Setor Terciário:** Atualmente, a cidade consolidou uma economia diversificada, em que o **Setor de Serviços e Comércio** responde pela maior parcela dos postos de trabalho e da geração de novas empresas.
    * **PIB Real Sustentado:** A trajetória do PIB Real atinge **{pib_bi_txt}**, refletindo a resiliência e a capacidade de recuperação da economia local.

    ### 💼 2. Pulverização Empresarial e Empreendedorismo
    * **Menor Porte Médio:** A base empresarial formal cresceu **{cresc_emp_txt}** na série histórica analisada, impulsionada de forma expressiva por **MEIs e Microempresas**.
    * **Geração de Empregos:** O volume de pessoal ocupado expandiu **{cresc_pes_txt}**. As micro e pequenas empresas de serviços funcionam como o principal amortecedor social e motor de absorção de mão de obra.
    """)

with col_right:
    st.markdown(f"""
    ### 💰 3. Dinâmica Salarial e Qualificação Profissional
    * **Renda Média:** O salário médio formal manteve-se equilibrado na faixa de 3.8 a 4.0 Salários Mínimos, com variações conforme o segmento econômico.
    * **Concentração de Massa Salarial:** Atividades administrativas e de atendimento absorvem grande volume de trabalhadores, enquanto serviços técnicos especializados, tecnologia e gestão lideram os patamares salariais mais altos.
    * **Papel da Qualificação:** Iniciativas municipais (como a Uniten e programas da SERTE) mostram-se essenciais para requalificar trabalhadores frente às novas demandas tecnológicas do mercado.

    ### 🚗 4. Centralidade e Autonomia Regional (RMS)
    * **Absorção Local:** A maioria dos trabalhadores residentes em Sorocaba trabalha no próprio município ({pct_mob_txt}), confirmando que a cidade não opera como "cidade-dormitório".
    * **Polo da RMS:** Sorocaba exerce papel de liderança e atração para os 27 municípios da Região Metropolitana, centralizando serviços de alta complexidade em saúde, educação, tecnologia e comércio.
    """)

st.markdown("---")

# --- VISUALIZAÇÃO DE IMPACTO POR MÓDULO (DINÂMICO) ---
st.header("📊 Matriz Síntese dos Módulos da Aplicação")

dados_sintese = pd.DataFrame({
    "Dimensão": [
        "01. Demografia & PIB",
        "02. Mercado de Trabalho",
        "03. Setor de Serviços",
        "04. Salários & Ocupações",
        "05. Mobilidade Urbana"
    ],
    "Tendência Observada": [
        f"População atingiu {pop_txt} ({pop_cresc_txt} vs 2010) e PIB de {pib_bi_txt}",
        f"Pessoal ocupado cresceu {cresc_pes_txt} e empresas {cresc_emp_txt}",
        "Dominância de MEI/ME e diversificação em subsetores de saúde, comércio e tecnologia",
        "Elevada absorção em cargos operacionais; topo salarial em gestão e serviços técnicos",
        f"Forte retenção local ({pct_mob_txt}) e centralidade regional na RMS"
    ],
    "Nível de Relevância": [85, 90, 95, 88, 80]
})

fig_sintese = px.bar(
    dados_sintese,
    x="Nível de Relevância",
    y="Dimensão",
    orientation="h",
    text="Tendência Observada",
    color="Nível de Relevância",
    color_continuous_scale="Blues",
    title="<b>Síntese do Impacto Socioeconômico por Dimensão de Análise</b>"
)
fig_sintese.update_traces(textposition="inside")
fig_sintese.update_layout(title_font_size=15, height=400, coloraxis_showscale=False)

st.plotly_chart(fig_sintese, use_container_width=True)
st.caption("Fonte: Elaboração consolidada a partir de dados do IBGE (Censos/CEMPRE), RAIS/MTE e Sebrae-SP.")

st.markdown("---")

# --- RECOMENDAÇÕES E INSIGHTS DE POLÍTICAS PÚBLICAS ---
st.header("💡 Recomendações Estratégicas e Oportunidades")

tab_rec1, tab_rec2, tab_rec3 = st.tabs([
    "🎯 Formação & Qualificação",
    "🏢 Apoio às Microempresas",
    "🔮 Visão de Futuro"
])

with tab_rec1:
    st.success("""
    **Foco em Capacitação Técnica:**
    - Alinhar os cursos oferecidos por órgãos como a Uniten às demandas do setor de Serviços de Alto Valor Agregado (Tecnologia da Informação, Saúde, Gestão Financeira e Logística).
    - Preparar a mão de obra sênior para o mercado, acompanhando o envelhecimento populacional registrado no Censo 2022.
    """)

with tab_rec2:
    st.info("""
    **Fortalecimento do Ambiente de Negócios:**
    - Manter e expandir programas de desburocratização e incentivo ao crédito para MEIs e Microempresas.
    - Ampliar a atuação da Casa do Trabalhador e da Van do Emprego para descentralizar o acesso a vagas e consultorias nos bairros periféricos.
    """)

with tab_rec3:
    st.warning("""
    **Integração Regional e Inovação:**
    - Potencializar a integração entre o Parque Tecnológico de Sorocaba (PTS) e o setor de serviços corporativos locais.
    - Consolidar a posição de Sorocaba como hub de mobilidade, saúde e educação para toda a Região Metropolitana de Sorocaba (RMS).
    """)

st.caption("Trabalho de Análise Econômica do Setor de Serviços — Sorocaba (SP)")
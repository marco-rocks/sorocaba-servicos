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

ANO_MAX = 2025  # teto da série histórica

st.title("💼 Estrutura do Mercado de Trabalho Formal")
st.markdown("Análise da evolução temporal do número de empresas, postos de trabalho, massa salarial em Sorocaba e comparação regional com municípios vizinhos do Estado de São Paulo.")

@st.cache_data
def carregar_dados():
    filepath_emp = PROCESSED_DIR / "empresas_empregos_limpo.csv"
    filepath_mun = PROCESSED_DIR / "empregados_total_municipios.csv"
    
    df_emp = pd.read_csv(filepath_emp) if filepath_emp.exists() else None
    df_mun = pd.read_csv(filepath_mun, sep=";") if filepath_mun.exists() else None
    
    return df_emp, df_mun

try:
    df_emp, df_mun = carregar_dados()

    if df_emp is None:
        st.error("⚠️ O arquivo `empresas_empregos_limpo.csv` não foi encontrado em `data/processed/`. Por favor, execute primeiro o script `python src/tratamento.py`.")
    else:
        # Ordenar a série histórica por ano
        df_emp = df_emp[df_emp["Ano"] <= ANO_MAX]
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
            delta=f"+{cresc_pessoal:.1f}% vs {ano_pri}".replace(".", ",")
        )
        col2.metric(
            label=f"Empresas Formais ({ano_ult})", 
            value=f"{int(ult_linha['Empresas']):,}".replace(",", "."), 
            delta=f"+{cresc_empresas:.1f}% vs {ano_pri}".replace(".", ",")
        )
        col3.metric(
            label=f"Pessoal Assalariado ({ano_ult})", 
            value=f"{int(ult_linha['Pessoal Assalariado']):,}".replace(",", ".")
        )
        col4.metric(
            label=f"Salário Médio ({ano_ult})", 
            value=f"{ult_linha['Salário Médio (S.M.)']:.1f}".replace(".", ",") + " S.M."
        )

        st.markdown("---")

        # --- GRÁFICO 1: EVOLUÇÃO DO EMPREGO FORMAL ---
        st.subheader("📈 Trajetória do Emprego Formal em Sorocaba")
        st.markdown("Comparativo entre o volume total de **Pessoal Ocupado** (inclui sócios e proprietários) e o **Pessoal Assalariado** formal.")

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
            title="<b>Evolução do Pessoal Ocupado Total vs. Pessoal Assalariado (2006–2021)</b>",
            labels={"Trabalhadores": "Número de Pessoas", "Ano": "Ano"}
        )
        fig_emp.update_traces(line_width=3, marker_size=7)
        fig_emp.update_layout(
            title_font_size=15,
            separators=",.",
            xaxis=dict(dtick=1, tickmode="linear"),
            yaxis=dict(tickformat="."),
            height=430,
            hovermode="x unified"
        )
        st.plotly_chart(fig_emp, use_container_width=True)
        st.caption("Fonte: IBGE — Cadastro Central de Empresas (CEMPRE).")

        st.markdown("---")

        # --- PAINEL DUPLO: EMPRESAS E SALÁRIOS ---
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("🏢 Crescimento do Total de Empresas Formais")
            df_emp["Empresas_Rotulo"] = df_emp["Empresas"].apply(lambda v: f"{int(v):,}".replace(",", "."))
            fig_emp_bar = px.bar(
                df_emp,
                x="Ano",
                y="Empresas",
                text="Empresas_Rotulo",
                title="<b>Empresas Formais Ativas em Sorocaba (CEMPRE)</b>",
                labels={"Empresas": "Qtd. de Empresas", "Ano": "Ano"},
                color_discrete_sequence=["#1f77b4"]
            )
            fig_emp_bar.update_traces(textposition="outside")
            fig_emp_bar.update_layout(
                title_font_size=15,
                separators=",.",
                xaxis=dict(dtick=1, tickmode="linear"), 
                yaxis=dict(tickformat="."),
                height=420
            )
            st.plotly_chart(fig_emp_bar, use_container_width=True)
            st.caption("Fonte: IBGE — Cadastro Central de Empresas (CEMPRE).")

        with col_r:
            st.subheader("💵 Evolução da Remuneração Média Formal")
            df_emp["Sal_Rotulo"] = df_emp["Salário Médio (S.M.)"].apply(lambda v: f"{v:.1f}".replace(".", ",") + " S.M.")
            fig_sal = px.line(
                df_emp,
                x="Ano",
                y="Salário Médio (S.M.)",
                text="Sal_Rotulo",
                markers=True,
                title="<b>Salário Médio Mensal em Salários Mínimos (S.M.)</b>",
                labels={"Salário Médio (S.M.)": "Salários Mínimos (S.M.)", "Ano": "Ano"},
                color_discrete_sequence=["#2ca02c"]
            )
            fig_sal.update_traces(line_width=3, marker_size=8, textposition="top center")
            fig_sal.update_layout(
                title_font_size=15,
                xaxis=dict(dtick=1, tickmode="linear"), 
                height=420
            )
            st.plotly_chart(fig_sal, use_container_width=True)
            st.caption("Fonte: IBGE — Cadastro Central de Empresas (CEMPRE).")

        # --- ANÁLISE: CRESCIMENTO TOTAL DE EMPRESAS ---
        st.markdown("---")
        st.header("🔍 Dinâmica Anual: Variação de Empresas vs. Empregos")

        df_an = df_emp[["Ano", "Empresas", "Pessoal Ocupado"]].copy()
        df_an["Var. Empresas (%)"] = df_an["Empresas"].pct_change() * 100
        df_an["Var. Pessoal Ocupado (%)"] = df_an["Pessoal Ocupado"].pct_change() * 100
        df_an["Saldo de Empresas"] = df_an["Empresas"].diff()
        df_an["Pessoas por Empresa"] = df_an["Pessoal Ocupado"] / df_an["Empresas"]

        n_anos = ano_ult - ano_pri
        cagr_emp = ((ult_linha["Empresas"] / pri_linha["Empresas"]) ** (1 / n_anos) - 1) * 100
        cagr_pes = ((ult_linha["Pessoal Ocupado"] / pri_linha["Pessoal Ocupado"]) ** (1 / n_anos) - 1) * 100

        a1, a2, a3 = st.columns(3)
        a1.metric("Crescimento Médio Anual (Empresas)", f"{cagr_emp:.2f}".replace(".", ",") + "% a.a.")
        a2.metric("Crescimento Médio Anual (Pessoal Ocupado)", f"{cagr_pes:.2f}".replace(".", ",") + "% a.a.")
        a3.metric("Saldo Líquido de Empresas Formais", f"{int(ult_linha['Empresas'] - pri_linha['Empresas']):,}".replace(",", "."))

        df_var = df_an.dropna(subset=["Var. Empresas (%)"]).copy()
        df_var["Rotulo_Var"] = df_var["Var. Empresas (%)"].apply(lambda v: f"{v:+.1f}%".replace(".", ","))

        c_l, c_r = st.columns(2)
        with c_l:
            fig_var = px.bar(
                df_var, x="Ano", y="Var. Empresas (%)", text="Rotulo_Var",
                title="<b>Variação Anual Percentual do Número de Empresas (%)</b>",
                color="Var. Empresas (%)", color_continuous_scale="RdYlGn"
            )
            fig_var.update_traces(textposition="outside")
            fig_var.update_layout(title_font_size=15, xaxis=dict(dtick=1, tickmode="linear"), height=420, coloraxis_showscale=False)
            st.plotly_chart(fig_var, use_container_width=True)
            st.caption("Fonte: Elaboração própria com base em CEMPRE/IBGE.")

        with c_r:
            df_cmp = df_var.melt(
                id_vars=["Ano"], value_vars=["Var. Empresas (%)", "Var. Pessoal Ocupado (%)"],
                var_name="Indicador", value_name="Variação (%)"
            )
            fig_cmp = px.line(
                df_cmp, x="Ano", y="Variação (%)", color="Indicador", markers=True,
                title="<b>Empresas vs. Pessoal Ocupado: Variação Anual Comparada (%)</b>"
            )
            fig_cmp.update_layout(title_font_size=15, xaxis=dict(dtick=1, tickmode="linear"), height=420, hovermode="x unified")
            st.plotly_chart(fig_cmp, use_container_width=True)
            st.caption("Fonte: Elaboração própria com base em CEMPRE/IBGE.")

        # --- SEÇÃO 3: COMPARAÇÃO REGIONAL COM OUTRAS CIDADES DO ESTADO ---
        if df_mun is not None and not df_mun.empty:
            st.markdown("---")
            st.subheader("🌐 Comparação Regional: Dinâmica do Emprego Formal na Região de Sorocaba")
            st.markdown("""
            O gráfico comparativo abaixo confronta a trajetória de geração de postos de trabalho formais de **Sorocaba** 
            com outras cidades da sua macrorregião no Estado de São Paulo (**Itu**, **Salto** e **Araçoiaba da Serra**), revelando a magnitude polarizadora da sede metropolitana.
            """)

            df_mun_pivot = df_mun.copy()
            df_mun_pivot["ano"] = pd.to_numeric(df_mun_pivot["ano"], errors="coerce").astype(int)
            df_mun_pivot["empregados_total"] = pd.to_numeric(df_mun_pivot["empregados_total"], errors="coerce")
            
            fig_comp_mun = px.line(
                df_mun_pivot,
                x="ano",
                y="empregados_total",
                color="municipio",
                markers=True,
                title="<b>Comparação de Empregados Formais Totais por Município (2016–2025)</b>",
                labels={"empregados_total": "Total de Empregados", "ano": "Ano", "municipio": "Município"},
                color_discrete_map={
                    "Sorocaba": "#1f77b4",
                    "Itu": "#ff7f0e",
                    "Salto": "#2ca02c",
                    "Araçoiaba da Serra": "#d62728"
                }
            )
            fig_comp_mun.update_traces(line_width=3, marker_size=7)
            fig_comp_mun.update_layout(
                title_font_size=15,
                separators=",.",
                xaxis=dict(tickmode="linear", dtick=1),
                yaxis=dict(tickformat="."),
                height=480,
                hovermode="x unified"
            )
            st.plotly_chart(fig_comp_mun, use_container_width=True)
            st.caption("Fonte: MTE / RAIS / CAGED — Painel comparativo de empregos formais totais por município.")

        # --- PAINEL DE SÍNTESE ---
        st.markdown("---")
        st.info("""
        💡 **Destaques do Mercado de Trabalho Formal:**
        - **Expansão do Emprego:** O pessoal ocupado saltou de **156,1 mil** (2006) para **237,3 mil** (2021) no CEMPRE, atingindo mais de **261,5 mil vínculos** na RAIS recente, demonstrando forte tração do setor terciário.
        - **Liderança Regional Incontestável:** Sorocaba concentra volume de postos formais quase 4 vezes maior que Itu (70,0 mil) e quase 7 vezes superior a Salto (37,8 mil), confirmando seu papel como polo de absorção de mão de obra de toda a RMS.
        - **Crescimento Empresarial Contínuo:** A base de empresas formais ativas avançou de **18,5 mil** para mais de **29,4 mil** estabelecimentos, puxada por micro e pequenas empresas de prestação de serviços.
        """)

except Exception as e:
    st.error(f"Erro ao processar a página: {e}")

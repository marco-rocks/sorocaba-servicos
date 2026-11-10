import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="07 — Metodologia ETL",
    page_icon="⚙️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROC_DIR = BASE_DIR / "data" / "processed"

st.title("⚙️ Metodologia e Pipeline de Engenharia de Dados (ETL)")
st.markdown("""
Documentação técnica e conceitual dos procedimentos de **Extração (Extract)**, **Transformação (Transform)** e **Carga (Load)** 
adotados para transformar dados brutos e heterogêneos de fontes governamentais em uma base analítica de alta performance para o Streamlit.
""")

st.markdown("---")

# --- DIAGRAMA DO PIPELINE ---
st.subheader("🔄 Arquitetura do Pipeline de Dados")

st.markdown("""
```mermaid
flowchart LR
    subgraph S1["1. Fontes de Extração (Raw Data)"]
        IBGE["IBGE / SIDRA<br/>(Censos 2010 e 2022)"]
        CEMPRE["IBGE / CEMPRE<br/>(Empresas & Pessoal)"]
        RAIS["MTE / RAIS & CAGED<br/>(Microdados CBO)"]
        SEBRAE["Receita Federal / Sebrae<br/>(MEIs & Novos Negócios)"]
    end

    subgraph S2["2. Pipeline de Transformação (src/tratamento.py)"]
        LIMPEZA["Sanitização & Encodings<br/>(UTF-8 / Latin1 / Delimitadores)"]
        TIPAGEM["Casting & Tipagem Numérica<br/>(Monetário, Inteiros, Pct)"]
        DEFLACAO["Deflacionamento pelo IPCA<br/>(Preços Constantes de 2023)"]
        METRICAS["Engenharia de Features<br/>(TGCA, CAGR, Saldos e Ranks)"]
    end

    subgraph S3["3. Camada Analítica de Carga (Processed & App)"]
        PARQUET["CSVs Estruturados & Otimizados<br/>(data/processed/)"]
        ST_CACHE["Streamlit Engine<br/>(@st.cache_data & Memória)"]
        DASH["Visualizações & KPIs Interativos<br/>(Plotly Express / Scatter Map)"]
    end

    IBGE --> LIMPEZA
    CEMPRE --> LIMPEZA
    RAIS --> LIMPEZA
    SEBRAE --> LIMPEZA

    LIMPEZA --> TIPAGEM
    TIPAGEM --> DEFLACAO
    DEFLACAO --> METRICAS

    METRICAS --> PARQUET
    PARQUET --> ST_CACHE
    ST_CACHE --> DASH
```
""")

st.markdown("---")

# --- DETALHAMENTO DAS ETAPAS DO ETL ---
tab_e, tab_t, tab_l, tab_code = st.tabs([
    "📥 1. Extração (Extract)",
    "🧪 2. Transformação (Transform)",
    "💾 3. Carga & Otimização (Load)",
    "💻 4. Código do Script (Pipeline)"
])

with tab_e:
    st.subheader("📥 1. Extração e Origem das Fontes")
    st.markdown("""
    Os dados brutos foram obtidos a partir de diferentes repositórios de estatísticas oficiais do governo brasileiro, apresentando grande disparidade de formatos, delimitadores (`,` e `;`) e codificações (`utf-8` e `latin-1`):
    
    * **IBGE - Censo Demográfico (2010 e 2022):** Extração de tabelas censitárias via plataforma SIDRA/IBGE com cruzamento de variáveis de faixas etárias e deslocamento pendular (`Censo 2010 - Sorocaba.csv`, `populacao_comparativo.csv`).
    * **IBGE - CEMPRE (Cadastro Central de Empresas):** Série temporal histórica de estabelecimentos formais, unidades locais, pessoal ocupado, pessoal assalariado e massa salarial (`empresas_empregos_formais.csv`).
    * **Fundação SEADE / IBGE - Contas Regionais:** Dados do Produto Interno Bruto (PIB) municipal nominal acompanhados de índices de inflação (`pib_tratado.csv`).
    * **MTE - RAIS (Relação Anual de Informações Sociais):** Microdados agregados por Código Brasileiro de Ocupações (CBO), com contagem de vínculos formais ativos e remuneração média mensal (`cbo_ocupacoes.csv`).
    * **Receita Federal / Sebrae-SP:** Registros de aberturas de pessoas jurídicas por porte empresarial (MEI, Microempresa, EPP) e estabelecimentos ativos por divisão da CNAE 2.0.
    """)

with tab_t:
    st.subheader("🧪 2. Limpeza, Tratamento e Engenharia de Features")
    st.markdown("""
    A fase de transformação executada pelo script [`src/tratamento.py`](file:///C:/Users/Marco/Desktop/lo-files/computher%20showt/sorocaba-servicos/src/tratamento.py) e pelas funções analíticas das telas inclui:
    
    1. **Padronização de Encodings e Delimitadores:**
       - Tratamento de caracteres latinos (acentos, cedilhas) resolvendo incompatibilidades entre Windows-1252/Latin-1 e UTF-8.
       - Conversão segura de separadores decimais e de milhar (remoção de pontos de milhar e substituição de vírgula por ponto decimal para processamento numérico).
    
    2. **Deflacionamento Monetário (Preços Constantes de 2023):**
       - Para neutralizar a ilusão inflacionária no PIB municipal, os valores nominais do PIB foram deflacionados pelo **IPCA acumulado**, trazendo toda a série histórica para **preços constantes de 2023**:
         $$\\text{PIB Real}_{2023} = \\text{PIB Nominal}_t \\times \\text{Fator de Reajuste}_t$$
    
    3. **Cálculo da TGCA (Taxa Geométrica de Crescimento Anual):**
       - No módulo de ocupações e empregos, aplicou-se a fórmula de taxa anualizada composta (CAGR):
         $$\\text{TGCA} = \\left( \\frac{V_{\\text{final}}}{V_{\\text{inicial}}} \\right)^{\\frac{1}{n}} - 1$$
       - Evita flutuações sazonais bruscas e permite comparar profissões com ritmos de expansão estruturalmente distintos.
    
    4. **Tratamento Categórico de Portes e MEI:**
       - Expressões regulares (`regex`) para classificar uniformemente Microempreendedores Individuais, Microempresas e EPPs, além de tratar campos nulos ou registros sem movimentação econômica ativa.
    """)

with tab_l:
    st.subheader("💾 3. Carga, Persistência e Performance no Streamlit")
    st.markdown("""
    Para garantir resposta instantânea na interface gráfica do usuário, a carga segue uma estratégia de cache de memória e pré-processamento desacoplado:
    
    * **Desacoplamento Batch vs. Serving:**
      - As transformações pesadas são executadas previamente e persistidas em arquivos CSV estruturados no diretório `data/processed/`.
      - O Streamlit não reprocessa matrizes brutas do zero a cada clique ou mudança de filtro do usuário.
    * **Memoization e Caching (`@st.cache_data`):**
      - As funções leitoras (`carregar_dados`) utilizam o decorador `@st.cache_data` do Streamlit, serializando os DataFrames em memória RAM após a primeira leitura.
    * **Formatação Visual Customizada:**
      - Aplicação de separadores numéricos adequados na camada de apresentação (`.` para milhar e `,` para decimal), assegurando conformidade com as normas ABNT sem comprometer os cálculos matemáticos subjacentes.
    """)

with tab_code:
    st.subheader("💻 4. Estrutura do Script de Tratamento (`src/tratamento.py`)")
    st.markdown("Trecho representativo dos procedimentos de transformação e sanitização do pipeline:")
    
    st.code("""
# Trecho de src/tratamento.py
def tratar_pib(filepath_raw: Path) -> pd.DataFrame:
    df = pd.read_csv(filepath_raw, sep=";", encoding="utf-8")
    
    # Conversão e limpeza de moeda para float
    for col in ["PIB Nominal (R$)", "PIB Real 2023 (R$)"]:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace("R$", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .str.strip().astype(float)
            )
            
    # Conversão de taxas inflacionárias
    for col in ["IPCA (%)", "Fator Reajuste", "Crescimento Real (%)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ".", regex=False).str.strip(),
                errors="coerce"
            )

    df["Ano"] = df["Ano"].astype(int)
    return df.sort_values("Ano").reset_index(drop=True)
    """, language="python")

st.markdown("---")

# --- RESUMO DOS ARQUIVOS PROCESSADOS ---
st.subheader("📁 Arquivos Gerados no Pipeline (`data/processed/`)")

tabela_arquivos = pd.DataFrame({
    "Arquivo Processado": [
        "pib_limpo.csv",
        "populacao_limpo.csv",
        "empresas_empregos_limpo.csv",
        "rais_ocupacoes_limpo.csv",
        "estabelecimentos_servicos.csv",
        "pessoas_servicos.csv",
        "novos_negocios.csv",
        "empregados_total_municipios.csv"
    ],
    "Fonte Primária": [
        "IBGE / Fundação SEADE",
        "IBGE (Censos 2010 e 2022)",
        "IBGE / CEMPRE",
        "MTE / RAIS",
        "CNAE / Estabelecimentos",
        "MTE / RAIS Serviços",
        "Receita Federal / Sebrae-SP",
        "MTE / RAIS / CAGED"
    ],
    "Variáveis / Métricas Chave": [
        "Ano, PIB Nominal, IPCA, Fator, PIB Real 2023, Crescimento Real",
        "Faixa Etária, População 2010, População 2022, Variação, % Crescimento",
        "Ano, Unidades Locais, Empresas, Pessoal Ocupado/Assalariado, Salário Médio",
        "Ano, CBO, Ocupação, Vínculos Formais, Salário Médio Nominal",
        "Divisão CNAE, Tipo de Serviço, Quantidade de Estabelecimentos Ativos",
        "Ano, Divisão CNAE, Pessoal Empregado em Serviços",
        "Ano, Porte Empresarial (MEI, ME, EPP), Quantidade de Aberturas",
        "Ano, Município (Sorocaba, Itu, Salto, Araçoiaba), Total de Empregados"
    ]
})

st.dataframe(tabela_arquivos, use_container_width=True, hide_index=True)
st.caption("Pipeline ETL implementado em Python com arquitetura modular desacoplada.")

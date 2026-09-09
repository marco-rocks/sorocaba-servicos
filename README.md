# 🏢 Setor de Serviços e Mercado de Trabalho em Sorocaba

Análise exploratória do papel do setor de serviços na dinâmica econômica e no mercado de trabalho do município de Sorocaba-SP.

---

## 🎯 Objetivo

Investigar a relevância e a participação do **setor de serviços** na economia e na geração de empregos no município de Sorocaba-SP, avaliando:

* **Dimensão do setor:** Representatividade no PIB municipal e no volume de estabelecimentos.
* **Distribuição dos empregos:** Alocação dos trabalhadores entre os diferentes subsetores de serviços.
* **Ocupações e remuneração:** Identificação das principais ocupações e análise dos níveis de remuneração.
* **Perfil do mercado de trabalho:** Caracterização dos trabalhadores empregados no setor.
* **Influência regional:** Análise do papel de Sorocaba como polo econômico e de serviços na Região Metropolitana de Sorocaba (RMS).
* **Evolução temporal:** Identificação de tendências e mudanças na participação do setor ao longo dos anos.

---

## 🛠️ Tecnologias Utilizadas

* **Python** — Linguagem base para processamento e análise dos dados.
* **Pandas** — Manipulação, limpeza e agregação das bases de dados.
* **Plotly** — Construção de gráficos e visualizações interativas.
* **Streamlit** — Desenvolvimento do dashboard web interativo.
* **Jupyter Notebook** — Exploração inicial e validação das análises.
* **Git/GitHub** — Versionamento e documentação do projeto.

---

## 🗃️ Fontes de Dados

O projeto utiliza dados públicos provenientes de fontes oficiais:

* **IBGE** — Indicadores econômicos, demográficos e territoriais.
* **CEMPRE — Cadastro Central de Empresas** — Informações sobre empresas e unidades locais.
* **RAIS — Relação Anual de Informações Sociais** — Informações sobre vínculos empregatícios, ocupações, remuneração e características dos trabalhadores.
* **Censo Demográfico** — Informações demográficas e socioeconômicas da população.

Os dados utilizados são públicos e foram tratados e estruturados especificamente para as análises apresentadas no projeto.

---

## 📁 Estrutura do Repositório

```text
sorocaba-servicos/
│
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📄 app.py
│
├── 📁 pages/                    # Páginas do dashboard Streamlit
│   ├── 01_contexto.py
│   ├── 02_mercado_trabalho.py
│   ├── 03_empregos_servicos.py
│   ├── 04_salarios.py
│   └── 05_mobilidade.py
│
├── 📁 src/                      # Código de processamento e análise
│   ├── __init__.py
│   │
│   ├── 📁 data/                 # Carregamento e preparação dos dados
│   │   ├── __init__.py
│   │   └── load.py
│   │
│   └── 📁 analysis/             # Funções e cálculos das análises
│       ├── __init__.py
│       ├── emprego.py
│       ├── servicos.py
│       ├── salarios.py
│       └── mobilidade.py
│
├── 📁 data/                     # Bases de dados utilizadas no projeto
│   ├── raw/                     # Dados brutos
│   │   └── .gitkeep
│   │
│   └── processed/               # Dados tratados
│       └── .gitkeep
│
└── 📁 assets/                   # Imagens e recursos visuais
    └── .gitkeep
```

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/marco-rocks/sorocaba-servicos.git
cd sorocaba-servicos
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute o dashboard

```bash
streamlit run app.py
```

Após a execução, o Streamlit disponibilizará o endereço local para acessar a aplicação pelo navegador.

---

## 🔎 Metodologia

O desenvolvimento do projeto é dividido em quatro etapas principais:

### 1. Coleta

Seleção e obtenção dos dados públicos disponibilizados pelas fontes oficiais.

### 2. Tratamento

Os dados são submetidos a processos de:

* Limpeza de valores ausentes;
* Padronização de nomes e categorias;
* Conversão de tipos;
* Filtragem dos municípios e atividades relevantes;
* Agregação dos indicadores;
* Criação de variáveis derivadas.

### 3. Análise

São calculados indicadores relacionados a:

* Emprego;
* Remuneração;
* Estabelecimentos;
* Participação econômica;
* Distribuição setorial;
* Evolução temporal;
* Comparações entre municípios.

### 4. Visualização

Os resultados são disponibilizados em um dashboard interativo desenvolvido com **Streamlit** e **Plotly**, permitindo explorar os dados por meio de filtros e diferentes perspectivas.

---

## 📌 Escopo

O projeto possui como foco principal:

> **Compreender a importância do setor de serviços para a economia e o mercado de trabalho de Sorocaba, relacionando o município ao contexto da Região Metropolitana de Sorocaba.**

A análise possui caráter **exploratório e descritivo**, buscando identificar padrões, diferenças e tendências nos dados, sem estabelecer relações causais que não possam ser sustentadas pelas bases utilizadas.

---

Este projeto foi desenvolvido para fins acadêmicos e educacionais.

Os dados utilizados pertencem às respectivas instituições responsáveis por sua disponibilização.

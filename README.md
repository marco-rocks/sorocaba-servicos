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

## ❓ Perguntas de Análise

O projeto busca responder, por meio dos dados, perguntas como:

1. Qual é a participação do setor de serviços na economia de Sorocaba?
2. Quais subsetores concentram a maior quantidade de empregos?
3. Quais são as principais ocupações dentro do setor de serviços?
4. Como a remuneração varia entre os diferentes subsetores e ocupações?
5. Quais atividades apresentam maior concentração de trabalhadores?
6. Como o mercado de trabalho de Sorocaba se compara ao contexto regional?
7. Sorocaba exerce um papel de concentração de empregos e serviços dentro da RMS?
8. Como esses indicadores evoluíram ao longo dos anos?

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

## 📊 Dashboard

A análise será apresentada por meio de uma aplicação interativa desenvolvida em **Streamlit**, permitindo explorar os principais indicadores do setor de serviços em Sorocaba.

### Principais análises

**Visão geral**

* Participação dos serviços na economia municipal;
* Número de estabelecimentos;
* Número de empregos;
* Indicadores gerais do mercado de trabalho.

**Mercado de trabalho**

* Distribuição dos empregos por subsetor;
* Principais ocupações;
* Remuneração média;
* Perfil dos trabalhadores.

**Análise regional**

* Comparação entre Sorocaba e municípios da RMS;
* Concentração de empregos e atividades;
* Participação de Sorocaba no contexto regional.

**Evolução temporal**

* Crescimento ou redução do emprego;
* Evolução da remuneração;
* Mudanças na composição do setor de serviços.

---

## 📁 Estrutura do Repositório

```text
sorocaba-servicos/
│
├── data/
│   ├── raw/                    # Dados brutos das fontes oficiais
│   └── processed/              # Dados tratados e prontos para análise
│
├── notebooks/                  # Análises exploratórias e validação dos dados
│
├── src/
│   ├── data_processing.py      # Funções de tratamento e preparação dos dados
│   └── visualization.py        # Funções para criação das visualizações
│
├── app.py                      # Aplicação principal em Streamlit
│
├── requirements.txt            # Dependências do projeto
│
└── README.md                   # Documentação do projeto
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

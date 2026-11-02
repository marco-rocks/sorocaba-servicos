import pandas as pd
from pathlib import Path

# BASE_DIR aponta para a raiz do projeto (sorocaba-servicos)
BASE_DIR = Path(__file__).resolve().parents[1]

# Diretórios de entrada (raw)
RAW_CONTEXTO_DIR = BASE_DIR / "data" / "raw" / "contexto"
RAW_MERCADO_DIR = BASE_DIR / "data" / "raw" / "mercado_trabalho"
RAW_SERVICOS_DIR = BASE_DIR / "data" / "raw" / "servicos"

# Diretório de saída (processed)
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def tratar_pib(filepath_raw: Path) -> pd.DataFrame:
    """Trata a série histórica do PIB de Sorocaba."""
    df = pd.read_csv(filepath_raw, sep=";", encoding="utf-8")
    
    # Conversão de valores monetários
    for col in ["PIB Nominal (R$)", "PIB Real 2023 (R$)"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("R$", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .str.strip()
                .astype(float)
            )
            
    # Conversão de taxas e percentuais
    for col in ["IPCA (%)", "Fator Reajuste", "Crescimento Real (%)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ".", regex=False).str.strip(),
                errors="coerce"
            )

    df["Ano"] = df["Ano"].astype(int)
    return df.sort_values("Ano").reset_index(drop=True)


def tratar_populacao(filepath_raw: Path) -> pd.DataFrame:
    """Trata os dados comparativos de população (Censo 2010 vs 2022)."""
    df = pd.read_csv(filepath_raw, sep=";", encoding="latin1")
    
    if "Crescimento (%)" in df.columns:
        df["Crescimento (%)"] = (
            df["Crescimento (%)"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
            .astype(float)
        )
        
    return df


def tratar_empresas_empregos(filepath_raw: Path) -> pd.DataFrame:
    """Trata a série histórica de empresas e empregos formais (CEMPRE)."""
    df = pd.read_csv(filepath_raw, sep=";", encoding="latin1", dtype=str)
    
    cols_contagem = [
        "Unidades Locais", "Empresas", 
        "Pessoal Ocupado", "Pessoal Assalariado", 
        "Salários (R$ Mil)"
    ]
    for col in cols_contagem:
        if col in df.columns:
            df[col] = df[col].str.replace(".", "", regex=False).str.strip().astype(int)
            
    if "Salário Médio (S.M.)" in df.columns:
        df["Salário Médio (S.M.)"] = (
            df["Salário Médio (S.M.)"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.strip()
            .astype(float)
        )
        
    df["Ano"] = df["Ano"].astype(int)
    return df.sort_values("Ano").reset_index(drop=True)


def tratar_ocupacoes_rais(filepath_raw: Path) -> pd.DataFrame:
    """Trata a base de ocupações CBO/RAIS."""
    df = pd.read_csv(filepath_raw)
    
    if "ano" in df.columns:
        df["ano"] = df["ano"].astype(int)
    if "trabalhadores" in df.columns:
        df["trabalhadores"] = df["trabalhadores"].astype(int)
        
    return df


def tratar_servicos_excel(filepath_raw: Path) -> pd.DataFrame:
    """Trata o ficheiro Excel do setor de serviços."""
    df_unidades = pd.read_excel(filepath_raw, sheet_name="unidades serviço - TRATADO")
    df_pessoas = pd.read_excel(filepath_raw, sheet_name="pessoas ocupado - TRATADO")
    
    df_unidades.columns = ["atividade", "unidades_locais", "ano"]
    df_pessoas.columns = ["atividade", "pessoal_ocupado", "ano"]
    
    for df, col in [(df_unidades, "unidades_locais"), (df_pessoas, "pessoal_ocupado")]:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .replace("-", "0")
            .replace("X", None)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df["ano"] = df["ano"].astype(int)

    return pd.merge(df_unidades, df_pessoas, on=["atividade", "ano"], how="outer")


if __name__ == "__main__":
    print("Iniciando o tratamento dos dados...\n")

    # 1. PIB
    f_pib = RAW_CONTEXTO_DIR / "pib_tratado.csv"
    if f_pib.exists():
        tratar_pib(f_pib).to_csv(PROCESSED_DIR / "pib_limpo.csv", index=False)
        print("✔ pib_limpo.csv gerado com sucesso!")

    # 2. População
    f_pop = RAW_CONTEXTO_DIR / "populacao_comparativo.csv"
    if f_pop.exists():
        tratar_populacao(f_pop).to_csv(PROCESSED_DIR / "populacao_limpo.csv", index=False)
        print("✔ populacao_limpo.csv gerado com sucesso!")

    # 3. Empresas e Empregos Formais
    f_emp = RAW_CONTEXTO_DIR / "empresas_empregos_formais.csv"
    if f_emp.exists():
        tratar_empresas_empregos(f_emp).to_csv(PROCESSED_DIR / "empresas_empregos_limpo.csv", index=False)
        print("✔ empresas_empregos_limpo.csv gerado com sucesso!")

    # 4. Ocupações / RAIS (cbo_ocupacoes.csv)
    f_cbo = RAW_MERCADO_DIR / "cbo_ocupacoes.csv"
    if f_cbo.exists():
        tratar_ocupacoes_rais(f_cbo).to_csv(PROCESSED_DIR / "rais_ocupacoes_limpo.csv", index=False)
        print("✔ rais_ocupacoes_limpo.csv gerado com sucesso!")

    # 5. Setor de Serviços (Excel - caso esteja na pasta raw/servicos)
    f_serv = RAW_SERVICOS_DIR / "empresas_servico_sorocaba.xlsx"
    if f_serv.exists():
        tratar_servicos_excel(f_serv).to_csv(PROCESSED_DIR / "servicos_detalhado_limpo.csv", index=False)
        print("✔ servicos_detalhado_limpo.csv gerado com sucesso!")

    print("\n--- Todos os ficheiros processados estão guardados em data/processed/ ---")
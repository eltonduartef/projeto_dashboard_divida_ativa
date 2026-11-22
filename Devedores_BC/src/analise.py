import pandas as pd

def resumo_geral(df: pd.DataFrame) -> dict:
    # Encontra o nome de quem tem a maior dívida individual (após agrupar por devedor)
    top_dev = (
        df.groupby("NOME DO DEVEDOR")["SALDO"]
          .sum()
          .sort_values(ascending=False)
    )
    
    maior_nome = top_dev.index[0] if not top_dev.empty else "N/A"
    maior_valor = top_dev.iloc[0] if not top_dev.empty else 0.0

    # Calcula o valor total suspenso por decisão judicial
    # (Filtra pela situação 'Suspenso' e motivo 'Decisão judicial')
    if "MOTIVO DA SUSPENSÃO" in df.columns:
        suspenso_judicial = df[
            (df["SITUACAO"] == "Suspenso") & 
            (df["MOTIVO DA SUSPENSÃO"].str.contains("judicial", case=False, na=False))
        ]["SALDO"].sum()
    else:
        suspenso_judicial = 0.0

    return {
        "total_registros": len(df),
        "total_devedores_unicos": df["CPF/CNPJ DEVEDOR"].nunique(),
        "valor_total": df["SALDO"].sum(),
        "ticket_medio": df["SALDO"].mean(),
        "maior_divida": df["SALDO"].max(),
        "pct_pessoa_fisica": (df["TIPO DE PESSOA"] == "Pessoa física").mean() * 100,
        # Novos campos:
        "maior_devedor_nome": maior_nome,
        "maior_devedor_valor": maior_valor,
        "valor_suspenso_judicial": suspenso_judicial,
    }

def top_devedores(df:pd.DataFrame, n: int = 15) -> pd.DataFrame:
    return(
        df.groupby(["NOME DO DEVEDOR", "CPF/CNPJ DEVEDOR"], as_index=False)["SALDO"].sum()
          .sort_values("SALDO", ascending=False)
          .head(n)
    )

def _agrupar(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    return (
        df.groupby(coluna)
          .agg(qtd=("SALDO", "size"), valor=("SALDO", "sum"))
          .sort_values("valor", ascending=False)
          .reset_index()
    )

def por_situacao(df):  return _agrupar(df, "SITUACAO")
def por_origem(df):    return _agrupar(df, "ORIGEM")

def por_ano(df:pd.DataFrame) -> pd.DataFrame:
    return(
        df.dropna(subset=["ANO_INSCRICAO"])
          .groupby("ANO_INSCRICAO")
          .agg(qtd=("SALDO", "size"), valor=("SALDO", "sum"))
          .reset_index()
          .sort_values("ANO_INSCRICAO")
    )

def top_credores(df:pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return(
        df.groupby("CREDOR")
          .agg(qtd=("SALDO", "size"), valor=("SALDO", "sum"))
          .sort_values("valor", ascending=False)
          .head(n)
          .reset_index()
    )
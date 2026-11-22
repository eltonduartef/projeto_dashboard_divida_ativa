import pandas as pd
import numpy as np

import pandas as pd
import numpy as np


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=";",
        encoding="latin-1",   # resolve "GERAÇĂO" -> "GERAÇÃO"
        dtype=str,
        keep_default_na=False,
    )
    df.columns = [c.strip() for c in df.columns]
    return df


def _parse_money(s: pd.Series) -> pd.Series:
    return (
        s.str.replace("R$", "", regex=False)
         .str.replace(".", "", regex=False)   # separador de milhar
         .str.replace(",", ".", regex=False)  # decimal
         .str.strip()
         .replace("", np.nan)
         .astype(float)
    )


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in ["DATA DE GERAÇÃO", "DATA DA INSCRIÇÃO"]:
        df[col] = pd.to_datetime(df[col], format="%d/%m/%Y %H:%M", errors="coerce")

    df["SALDO"] = _parse_money(df["SALDO DEVEDOR SEM HONORÁRIOS"])

    df["TIPO DE PESSOA"] = df["TIPO DE PESSOA"].str.strip()
    df["SITUACAO"]      = df["SITUAÇÃO DO CRÉDITO"].str.strip()
    df["ORIGEM"]        = df["ORIGEM"].str.strip()
    df["TIPO DEVEDOR"]  = df["TIPO DO DEVEDOR"].str.strip()
    df["ANO_INSCRICAO"] = df["DATA DA INSCRIÇÃO"].dt.year
    df["DOC_MASCARADO"] = df["CPF/CNPJ DEVEDOR"].str.startswith("XXX")

    return df


def load_and_clean(path: str) -> pd.DataFrame:
    return clean(load_data(path))   # Chama load_data + clean
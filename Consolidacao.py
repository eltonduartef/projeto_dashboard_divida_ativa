import pandas as pd
import plotly.express as px

dados = {
    "matricula": [1001, 1002, 1003, 1004, 1005, 1006, 1001, 1002, 1003, 1004, 1005, 1006],
    "bairro": ["Centro", "Jardim", "Praia", "Novo Horizonte", "Bela Vista", "Vila Nova",
               "Centro", "Jardim", "Praia", "Novo Horizonte", "Bela Vista", "Vila Nova"],
    "categoria": ["Residencial", "Comercial", "Residencial", "Industrial", "Residencial", "Comercial",
                  "Residencial", "Comercial", "Residencial", "Industrial", "Residencial", "Comercial"],
    "mes": ["Set"]*6 + ["Out"]*6,
    "leitura_anterior": [120, 340, 85, 900, 325, 210, 135, 362, 97, 950, 343, 233],
    "leitura_atual": [135, 362, 97, 950, 343, 233, 149, 385, 108, 1040, 360, 260],
}

df = pd.DataFrame(dados)
df["consumo"] = df["leitura_atual"] - df["leitura_anterior"]
print(df[(df["mes"] == "Out") & (df["consumo"] > 20)])
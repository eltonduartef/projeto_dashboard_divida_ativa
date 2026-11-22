import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

dados = {
    "matricula": [1001, 1002, 1003, 1004, 1005],
    "bairro": ["Centro", "Jardim", "Praia", "Novo Horizonte", "Bela Vista"],
    "categoria": ["Residencial", "Comercial", "Residencial", "Industrial", "Residencial"],
    "leitura_anterior": [120, 340, 85, 900, 325],
    "leitura_atual": [135, 362, 97, 950, 343]}
df = pd.DataFrame(dados)
df["consumo"] = df["leitura_atual"] - df["leitura_anterior"] 

totais = df.groupby(["matricula", "bairro"])["consumo"].sum().reset_index()
fig = px.bar(totais, x="matricula", y="consumo", title="Consumo por Matrícula", 
             color="consumo", color_discrete_sequence=["blue"]
             )
fig.write_html("consumo_matricula.html")
fig.show()
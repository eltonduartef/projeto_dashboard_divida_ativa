import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]          # .../Devedores_BC
sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# ---------- TEMPLATE PLOTLY CUSTOMIZADO ----------
custom_template = pio.templates["plotly_dark"]
custom_template.layout.paper_bgcolor = "rgba(0,0,0,0)" # Fundo externo transparente
custom_template.layout.plot_bgcolor = "rgba(0,0,0,0)"  # Fundo interno transparente
custom_template.layout.font.color = "#ecf0f1"          # Cor da fonte geral
custom_template.layout.title.font.size = 16            # Tamanho do título
custom_template.layout.colorway = [                    # Paleta de cores oficial
    "#3498db", # Azul claro
    "#e74c3c", # Vermelho
    "#f1c40f", # Amarelo
    "#1abc9c", # Verde água
    "#95a5a6"  # Cinza
]

pio.templates["custom_dark"] = custom_template
pio.templates.default = "custom_dark"

from src.limpeza import load_and_clean
from src import analise

# ---------- FUNÇÕES AUXILIARES ----------
def formatar_moeda(valor):
    if valor >= 1_000_000_000:
        return f"R$ {valor/1_000_000_000:,.1f} bi"
    elif valor >= 1_000_000:
        return f"R$ {valor/1_000_000:,.1f} mi"
    elif valor >= 1_000:
        return f"R$ {valor/1_000:,.1f} mil"
    else:
        return f"R$ {valor:,.2f}"

CSV_PATH = BASE_DIR / "data" / "DEVEDORES_DIVIDA_ATIVA-2024-12.csv"

@st.cache_data
def pegar_dados():
    return load_and_clean(str(CSV_PATH))

df = pegar_dados()

# ---------- CUSTOMIZAÇÃO VISUAL (CSS) ----------
st.markdown(
    """
    <style>
    /* 1. Cor de fundo geral (azul escuro corporativo) */
    .stApp {
        background-color: #1a252f;
    }
    
    /* 2. Força o texto geral a ser branco/claro */
    .stApp p, .stApp span, .stApp label, .stApp li {
        color: #ecf0f1 !important;
    }
    
    /* 3. Estilo da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* 4. Cartões de Métrica (KPIs) */
    [data-testid="stMetric"] {
        background-color: #2c3e50;
        border: 1px solid #34495e;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 5px solid #3498db;
    }
    
    /* 5. Títulos das seções */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding-bottom: 5px;
        border-bottom: 2px solid #34495e;
    }
    
    /* 6. Tabela de dados */
    [data-testid="stDataFrame"] {
        background-color: #2c3e50;
    }
    
    /* 7. Input de texto na sidebar (para não ficar invisível) */
    [data-testid="stSidebar"] input {
        background-color: #1a252f !important;
        color: white !important;
        border: 1px solid #34495e !important;
    }
    
    /* 8. Esconder menus do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- CABEÇALHO ----------
st.title("Painel de Devedores - Dívida Ativa")
st.markdown(
    """
    <p style='font-size: 1.1rem; color: #bdc3c7; margin-top: -15px; margin-bottom: 25px;'>
    Análise dos créditos inscritos em dívida ativa do Banco Central do Brasil (Base: Dez/2024)
    </p>
    """, 
    unsafe_allow_html=True
)

# ---------- SIDEBAR (FILTROS) ----------
st.sidebar.header("Filtros")

# Opções únicas
opcoes_situacao = sorted(df["SITUACAO"].dropna().unique())
opcoes_tipo = sorted(df["TIPO DE PESSOA"].dropna().unique())
opcoes_origem = sorted(df["ORIGEM"].dropna().unique())

# Criando os filtros com placeholder personalizado
situacoes = st.sidebar.multiselect(
    "Situação", 
    opcoes_situacao, 
    placeholder="Selecione..." # <- Aqui está o truque!
)

tipos = st.sidebar.multiselect(
    "Tipo de pessoa", 
    opcoes_tipo, 
    placeholder="Selecione..."
)

origens = st.sidebar.multiselect(
    "Origem", 
    opcoes_origem, 
    placeholder="Selecione..."
)

# Busca rápida
st.sidebar.subheader("Busca Rápida")
busca = st.sidebar.text_input("Nome do devedor", placeholder="Ex: Flamengo")

# ---------- APLICA OS FILTROS INTELIGENTES ----------
f = df.copy()

# Se o usuário não selecionou nada, usamos TODAS as opções (mostra tudo)
if situacoes:
    f = f[f["SITUACAO"].isin(situacoes)]
    
if tipos:
    f = f[f["TIPO DE PESSOA"].isin(tipos)]
    
if origens:
    f = f[f["ORIGEM"].isin(origens)]
    
if busca:
    f = f[f["NOME DO DEVEDOR"].str.contains(busca, case=False, na=False)]

# ---------- KPIs ----------
r = analise.resumo_geral(f)

# Linha 1: Visão Geral
c1, c2, c3 = st.columns(3)
c1.metric("Registros", f"{r['total_registros']:,}")
c2.metric("Devedores Únicos", f"{r['total_devedores_unicos']:,}")
c3.metric("Valor Total", formatar_moeda(r["valor_total"]))

# Linha 2: Destaques e Alertas
c4, c5, c6 = st.columns(3)
c4.metric("Ticket Médio", formatar_moeda(r["ticket_medio"]))
c5.metric("Maior Devedor Individual", 
          formatar_moeda(r["maior_devedor_valor"]), 
          help=r["maior_devedor_nome"])
c6.metric("Suspenso por Decisão Judicial", formatar_moeda(r["valor_suspenso_judicial"]))

# ---------- GRÁFICOS ----------

# 1. Top 15 devedores
st.subheader("Top 15 devedores")
top = analise.top_devedores(f, 15)
if not top.empty:
    fig = px.bar(
        top.sort_values("SALDO"), x="SALDO", y="NOME DO DEVEDOR",
        orientation="h", text_auto=".2s",
        title="Top 15 Maiores Devedores",
        color="SALDO", color_continuous_scale="Tealrose"
    )
    fig.update_layout(yaxis_title="", xaxis_title="Valor (R$)", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum devedor encontrado com os filtros atuais.")

# 2. Dívida Ativa: Clubes de Futebol
st.subheader("Dívida Ativa: Clubes de Futebol")
clubes_nomes = [
    "Clube de Regatas do Flamengo", "Botafogo de Futebol e Regatas", 
    "Sport Club Internacional", "Coritiba Foot Ball Club", 
    "Esporte Clube Vitoria", "Club de Regatas Vasco da Gama", 
    "Fluminense Football Club", "Sport Club Corinthians Paulista", 
    "Sociedade Esportiva Palmeiras", "Esporte Clube Santo Andre", 
    "Goias Esporte Clube"
]
mask_clubes = f["NOME DO DEVEDOR"].str.contains("|".join(clubes_nomes), case=False, na=False)
clubes = f[mask_clubes].groupby("NOME DO DEVEDOR", as_index=False)["SALDO"].sum()

if not clubes.empty:
    clubes = clubes.sort_values("SALDO", ascending=True).tail(10)
    fig_clubes = px.bar(
        clubes, x="SALDO", y="NOME DO DEVEDOR", orientation="h",
        text_auto=".2s", title="Top 10 Clubes com maior dívida (R$)",
        color="SALDO", color_continuous_scale="Reds"
    )
    fig_clubes.update_layout(yaxis_title="", xaxis_title="Valor (R$)", coloraxis_showscale=False)
    st.plotly_chart(fig_clubes, use_container_width=True)
else:
    st.info("Nenhum clube encontrado com os filtros atuais.")

# 3. Distribuição por Tipo de Devedor (Principal vs Corresponsável)
st.subheader("Distribuição por Tipo de Devedor")
tipo_devedor = f.groupby("TIPO DEVEDOR", as_index=False)["SALDO"].sum()

if not tipo_devedor.empty:
    fig_tipo = px.pie(
        tipo_devedor, names="TIPO DEVEDOR", values="SALDO", hole=0.5,
        title="Proporção do valor total",
        color="TIPO DEVEDOR",
        color_discrete_map={"Principal": "#3498db", "Corresponsável": "#e74c3c"}
    )
    fig_tipo.update_traces(textinfo='label+percent', textposition='inside')
    st.plotly_chart(fig_tipo, use_container_width=True)
else:
    st.info("Nenhum dado para os filtros atuais.")

# 4. Por situação e Por origem (Lado a Lado)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Por situação")
    s = analise.por_situacao(f)
    fig_situacao = px.pie(s, names="SITUACAO", values="valor", hole=0.5, title="Distribuição por Situação")
    fig_situacao.update_traces(textinfo='percent', textposition='inside')
    fig_situacao.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    st.plotly_chart(fig_situacao, use_container_width=True)

with col2:
    st.subheader("Por origem")
    o = analise.por_origem(f)
    fig_origem = px.bar(o, x="ORIGEM", y="valor", title="Distribuição por Origem")
    fig_origem.update_layout(xaxis_tickangle=0, xaxis_title="", yaxis_title="Valor (R$)")
    st.plotly_chart(fig_origem, use_container_width=True)

# 5. Evolução por ano e Distribuição Log (Lado a Lado)
col3, col4 = st.columns(2)
with col3:
    st.subheader("Evolução por ano")
    a = analise.por_ano(f)
    if not a.empty:
        fig_ano = px.line(a, x="ANO_INSCRICAO", y="valor", markers=True,
                          title="Evolução do Valor por Ano de Inscrição",
                          labels={"ANO_INSCRICAO": "Ano", "valor": "Valor Total (R$)"})
        st.plotly_chart(fig_ano, use_container_width=True)
    else:
        st.warning("Sem dados de ano para os filtros selecionados.")

with col4:
    st.subheader("Distribuição (escala log)")
    d = f[f["SALDO"] > 0].copy()
    d["log_saldo"] = np.log10(d["SALDO"])
    fig_hist = px.histogram(
        d, x="log_saldo", nbins=60, 
        title="Distribuição Logarítmica dos Saldos",
        labels={"log_saldo": "Log10 (Saldo)", "count": "Quantidade de Devedores"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ---------- TABELA DETALHADA E DOWNLOAD ----------
st.subheader("Tabela detalhada")
tabela = f[["NOME DO DEVEDOR","TIPO DE PESSOA","SITUACAO","ORIGEM","SALDO","DATA DA INSCRIÇÃO"]].sort_values("SALDO", ascending=False)
st.dataframe(tabela, use_container_width=True)

# Botão de download
csv = tabela.to_csv(index=False, sep=";").encode("utf-8-sig")
st.download_button(
    label="Baixar tabela filtrada (CSV)",
    data=csv,
    file_name="devedores_filtrados.csv",
    mime="text/csv"
)
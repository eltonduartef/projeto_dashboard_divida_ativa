# Painel de Devedores - Dívida Ativa (Banco Central)

Este projeto é um dashboard interativo desenvolvido em Python e Streamlit para analisar os dados abertos de Devedores da Dívida Ativa do Banco Central do Brasil (base de Dezembro/2024).

🔗 **[Clique aqui para acessar o Dashboard Online](https://divida-ativa-bc-elton.streamlit.app/)**

## Objetivo do Projeto
Transformar um arquivo CSV bruto e complexo em uma ferramenta visual capaz de responder perguntas de negócio, como: Quem são os maiores devedores? Qual a proporção de corresponsáveis? Qual o impacto dos clubes de futebol? Quanto está suspenso por decisões judiciais?

## Principais Insights Extraídos
*   **Concentração de Riqueza (e Dívida):** A dívida é fortemente concentrada em cauda longa. Poucos devedores (como grandes empresas em liquidação) concentram bilhões, enquanto a maioria deve valores na casa dos milhares.
*   **O Peso dos Corresponsáveis:** Embora os devedores "Principais" concentrem a maior parte do valor total, os maiores valores individuais muitas vezes estão nos "Corresponsáveis" (avalistas/sócios).
*   **Clubes de Futebol:** Um cluster temático interessante, mostrando que grandes clubes brasileiros possuem dívidas ativas milionárias.
*   **Litígio Judicial:** Há uma quantia significativa de dinheiro (centenas de milhões) "travada" na situação "Suspenso" aguardando decisões judiciais.

## Tecnologias Utilizadas
*   **Python 3.12**
*   **Pandas & NumPy:** Limpeza, transformação e análise dos dados.
*   **Streamlit:** Criação da interface web interativa.
*   **Plotly Express:** Construção dos gráficos interativos.
*   **Git & GitHub:** Versionamento de código.
*   **Streamlit Community Cloud:** Deploy da aplicação.

## Estrutura do Projeto
```text
Devedores_BC/
├── data/
│   └── DEVEDORES_DIVIDA_ATIVA-2024-12.csv
├── src/
│   ├── __init__.py
│   ├── limpeza.py      # ETL: Leitura e tratamento de nulos, datas e moedas
│   ├── analise.py      # Regras de negócio e agregações
│   └── dashboard.py    # Interface do usuário (Streamlit)
├── requirements.txt
└── README.md

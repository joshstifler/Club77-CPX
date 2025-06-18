import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Resumo de Vendas", layout="centered")

st.title("📦 Controle de Vendas - Resumo Diário")

# Valores fixos
PRECO_ICE = 200_000
CUSTO_ICE = 100_000

PRECO_GARRAFA = 50_000
CUSTO_GARRAFA = 15_000

# Entrada de dados
st.subheader("Informe as quantidades vendidas:")

qtd_ice = st.number_input("Quantidade de ICE 77", min_value=0, step=1)
qtd_garrafa = st.number_input("Quantidade de Garrafas", min_value=0, step=1)
qtd_outros = st.number_input("Quantidade de Outros", min_value=0, step=1)
valor_outros = st.number_input("Valor unitário de 'Outros'", min_value=0, step=1000)

# Cálculos
venda_ice = qtd_ice * PRECO_ICE
custo_ice = qtd_ice * CUSTO_ICE

venda_garrafa = qtd_garrafa * PRECO_GARRAFA
custo_garrafa = qtd_garrafa * CUSTO_GARRAFA

venda_outros = qtd_outros * valor_outros
custo_outros = 0  # pode ser alterado futuramente

total_venda = venda_ice + venda_garrafa + venda_outros
total_custo = custo_ice + custo_garrafa + custo_outros
lucro = total_venda - total_custo

# Geração do relatório
hoje = datetime.now().strftime('%d-%m-%Y')
relatorio = f"""RELATÓRIO DE VENDAS - {hoje}

Quantidade Vendida:
- ICE 77: {qtd_ice}
- Garrafas: {qtd_garrafa}
- Outros: {qtd_outros} (R$ {valor_outros:,} cada)

Totais:
- Total Vendido: R$ {total_venda:,}
- Total de Custo: R$ {total_custo:,}
- Total a Enviar: R$ {lucro:,}

>>> Enviar para Miranda Magnata ID-7684
"""

# Exibe resultado no app
st.markdown("---")
st.subheader("💰 Resultado do Dia")

col1, col2, col3 = st.columns(3)
col1.metric("Total Vendido", f"R$ {total_venda:,.0f}")
col2.metric("Total de Custo", f"R$ {total_custo:,.0f}")
col3.metric("Total a Enviar", f"R$ {lucro:,.0f}")

st.markdown("---")
st.text_area("Relatório gerado (copie e salve):", relatorio, height=200)

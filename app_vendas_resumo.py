import streamlit as st
from datetime import datetime
import requests
import base64

# ----- FUNÇÕES DE ESTILO -----
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

def show_logo(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{encoded}' width='150'></div>",
        unsafe_allow_html=True
    )

# ----- PROTEÇÃO POR SENHA -----
def login():
    st.title("🔒 Acesso Restrito - Club 77")
    senha = st.text_input("Digite a senha para continuar:", type="password")
    if senha == "club77acesso":
        st.session_state['autenticado'] = True
        st.success("✅ Acesso liberado!")
    else:
        st.stop()

if not st.session_state.get('autenticado'):
    login()

# ----- ESTILO E INTERFACE -----
set_background("club77_background_faded.png")
show_logo("club77_logo.png")
st.title("💎 Club 77 - Controle de Vendas")
st.markdown("---")

# ----- VALORES FIXOS -----
PRECO_ICE = 200_000
CUSTO_ICE = 100_000
PRECO_GARRAFA = 50_000
CUSTO_GARRAFA = 15_000

# ----- INÍCIO DO TURNO -----
vendedor = st.text_input("👤 Nome do Vendedor")

if st.button("✅ Iniciar Turno"):
    st.session_state['turno_ativo'] = True
    st.success("Turno iniciado!")

# ----- INTERFACE DE VENDA -----
if st.session_state.get('turno_ativo'):

    st.subheader("📦 Registro de Vendas")

    qtd_ice = st.number_input("Quantidade de ICE 77", min_value=0, step=1)
    qtd_garrafa = st.number_input("Quantidade de Garrafas", min_value=0, step=1)
    qtd_outros = st.number_input("Quantidade de Outros", min_value=0, step=1)
    valor_outros = st.number_input("Valor unitário de 'Outros'", min_value=0, step=1000)

    venda_ice = qtd_ice * PRECO_ICE
    custo_ice = qtd_ice * CUSTO_ICE

    venda_garrafa = qtd_garrafa * PRECO_GARRAFA
    custo_garrafa = qtd_garrafa * CUSTO_GARRAFA

    venda_outros = qtd_outros * valor_outros
    custo_outros = 0

    total_venda = venda_ice + venda_garrafa + venda_outros
    total_custo = custo_ice + custo_garrafa + custo_outros
    lucro = total_venda - total_custo

    st.markdown("---")
    st.subheader("💰 Resultado Parcial")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Vendido", f"R$ {total_venda:,.0f}")
    col2.metric("Total de Custo", f"R$ {total_custo:,.0f}")
    col3.metric("Total a Enviar", f"R$ {lucro:,.0f}")

    # ----- FINALIZAR TURNO -----
    if st.button("🚪 Finalizar Turno e Enviar Relatório"):
        hoje = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        relatorio = f"""📊 RELATÓRIO DE VENDAS - {hoje}

👤 Vendedor: {vendedor}

Quantidade Vendida:
- ICE 77: {qtd_ice}
- Garrafas: {qtd_garrafa}
- Outros: {qtd_outros} (R$ {valor_outros:,} cada)

Totais:
- Total Vendido: R$ {total_venda:,}
- Total de Custo: R$ {total_custo:,}
- Total a Enviar: R$ {lucro:,}

➡️ Enviar para Miranda Magnata ID-7684"""

        try:
            webhook_url = st.secrets["discord"]["webhook_url"]
            requests.post(webhook_url, json={"content": f"```{relatorio}```"})
            st.success("✅ Relatório enviado para o Discord!")
        except:
            st.error("❌ Erro ao enviar para o Discord.")

        st.session_state['turno_ativo'] = False

import streamlit as st
import json
import logging
from datetime import date, datetime

# Configuração de logs
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Nome do arquivo para salvar as tarefas
FILE_NAME = "tarefas.json"

# Função para carregar tarefas
def carregar_tarefas():
    try:
        with open(FILE_NAME, "r") as file:
            tarefas = json.load(file)
            # Adicionar campos padrão para tarefas antigas
            for tarefa in tarefas:
                if "prazo" not in tarefa:
                    tarefa["prazo"] = date.today().strftime("%Y-%m-%d")
                if "categoria" not in tarefa:
                    tarefa["categoria"] = "Sem categoria"
            logging.info("Tarefas carregadas com sucesso.")
            return tarefas
    except FileNotFoundError:
        logging.warning("Arquivo de tarefas não encontrado. Criando um novo.")
        return []
    except Exception as e:
        logging.error(f"Erro ao carregar tarefas: {e}")
        return []

# Função para salvar tarefas
def salvar_tarefas(tarefas):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tarefas, file, indent=4)
            logging.info("Tarefas salvas com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar tarefas: {e}")

# Carregar ou inicializar as tarefas
if "tarefas" not in st.session_state:
    st.session_state.tarefas = carregar_tarefas()

# Título do aplicativo
st.title("📋 Lista de Tarefas Avançada")

# Formulário para adicionar tarefas
with st.form("Adicionar Tarefa"):
    nova_tarefa = st.text_input("Digite a nova tarefa:")
    prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
    categoria = st.text_input("Categoria (ex.: Trabalho, Pessoal, Estudo):", value="Pessoal")
    prazo = st.date_input("Prazo:", value=date.today())
    submit = st.form_submit_button("Adicionar")

    if submit and nova_tarefa:
        st.session_state.tarefas.append({
            "tarefa": nova_tarefa,
            "prioridade": prioridade,
            "categoria": categoria,
            "prazo": prazo.strftime("%Y-%m-%d"),
            "concluida": False
        })
        salvar_tarefas(st.session_state.tarefas)
        logging.info(f"Tarefa adicionada: {nova_tarefa}, Prioridade: {prioridade}, Categoria: {categoria}, Prazo: {prazo}")
        st.success("Tarefa adicionada com sucesso!")

# Separador visual
st.markdown("---")

# Exibição das tarefas
st.subheader("📌 Suas Tarefas:")
for i, tarefa in enumerate(st.session_state.tarefas):
    # Garantir valores padrão para campos ausentes
    prazo_formatado = datetime.strptime(tarefa.get("prazo", date.today().strftime("%Y-%m-%d")), "%Y-%m-%d").strftime("%d/%m/%Y")
    categoria = tarefa.get("categoria", "Sem categoria")
    col1, col2, col3, col4 = st.columns([5, 2, 2, 1])
    col1.write(f"**{tarefa['tarefa']}**\nPrioridade: {tarefa['prioridade']}\nCategoria: {categoria}\nPrazo: {prazo_formatado}")
    if col2.button("✔️ Concluir", key=f"concluir_{i}"):
        st.session_state.tarefas[i]["concluida"] = True
        salvar_tarefas(st.session_state.tarefas)
        logging.info(f"Tarefa concluída: {tarefa['tarefa']}")
        st.experimental_rerun()
    if col3.button("🗑️ Remover", key=f"remover_{i}"):
        st.session_state.tarefas.pop(i)
        salvar_tarefas(st.session_state.tarefas)
        logging.info(f"Tarefa removida: {tarefa['tarefa']}")
        st.experimental_rerun()
    if tarefa["concluida"]:
        col4.markdown("✅")

# Separador visual
st.markdown("---")

# Estatísticas simples
st.subheader("📊 Estatísticas:")
total_tarefas = len(st.session_state.tarefas)
tarefas_concluidas = sum(tarefa["concluida"] for tarefa in st.session_state.tarefas)
tarefas_pendentes = total_tarefas - tarefas_concluidas
st.write(f"**Total de Tarefas:** {total_tarefas}")
st.write(f"**Tarefas Concluídas:** {tarefas_concluidas}")
st.write(f"**Tarefas Pendentes:** {tarefas_pendentes}")

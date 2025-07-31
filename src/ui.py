# src/ui.py
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st
from src.rag_pipeline import CodeAssistant  # Importa la classe che hai già creato

# --- Configurazione della Pagina ---
st.set_page_config(
    page_title="Assistente AI per la Codebase",
    page_icon="💻",
    layout="wide",  # Puoi provare "centered"
    initial_sidebar_state="expanded",
)

# --- Inizializzazione dell'Assistente AI (una sola volta per sessione) ---
if "code_assistant" not in st.session_state:
    with st.spinner(
        "Caricamento del modello AI e del database vettoriale... Potrebbe volerci un po'! 😉"
    ):
        try:
            st.session_state.code_assistant = CodeAssistant()
            st.success("Assistente AI pronto! 💪")
        except Exception as e:
            st.error(f"Errore durante l'inizializzazione dell'assistente AI: {e}")
            st.stop()

# Inizializza la cronologia della chat se non esiste.
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Opzioni e Informazioni")
    st.write(
        "Questo è un assistente AI che risponde a domande sulla tua codebase Java."
    )
    st.write("Il modello LLM è in esecuzione localmente sul tuo Mac M3.")
    st.markdown("---")
    st.subheader("Informazioni sul Modello")
    if "code_assistant" in st.session_state:
        st.info(
            f"""
            **Modello LLM:** Mistral-7B-Instruct-v0.2 (GGUF)
            **Embedding:** all-MiniLM-L6-v2
            **Database:** ChromaDB ({st.session_state.code_assistant.vectorstore._collection.count()} elementi indicizzati)
            """
        )
    st.markdown("---")
    if st.button(
        "Pulisci Cronologia",
        help="Cancella tutte le domande e risposte dalla cronologia.",
    ):
        st.session_state.messages = []
        st.experimental_rerun()  # Ricarica la pagina per mostrare la cronologia vuota

# --- Contenuto Principale ---
st.title("👨‍💻 Assistente AI per la Codebase Java")
st.markdown(
    "Fai domande sul tuo codice Java e l'AI cercherà le risposte nella codebase indicizzata."
)

# Mostra la cronologia della chat
# st.chat_message è lo standard per le interfacce di chat in Streamlit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Funzione per elaborare la domanda e ottenere la risposta dall'AI
def process_question(question_text: str):
    """Elabora una domanda, la aggiunge alla cronologia e ottiene la risposta dall'AI."""
    st.session_state.messages.append({"role": "user", "content": question_text})

    # Questo blocco viene mostrato durante il re-run causato dall'aggiunta del messaggio
    # e poi dalla generazione della risposta.
    with st.chat_message("assistant"):
        with st.spinner(f"L'AI sta elaborando la domanda: '{question_text}'..."):
            try:
                response = st.session_state.code_assistant.ask_codebase(question_text)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(
                    f"Si è verificato un errore durante la generazione della risposta: {e}"
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"Errore: {e}"}
                )


# Input dell'utente con st.chat_input
if prompt := st.chat_input(
    "Fai una domanda sul codice (es. 'Spiegami la classe OrderProcessor'):"
):
    process_question(prompt)  # Chiama la funzione di elaborazione

# --- Sezione Esempi di Domande ---
st.markdown("---")
st.subheader("💡 Esempi di domande per iniziare:")
example_questions = [
    "Descrivi la funzione principale del metodo 'saveUser'.",
    "Come vengono gestiti gli errori di database?",
    "Trova tutti gli utilizzi di 'Optional' nel codice e spiegali.",
    "Qual è il pattern di design predominante in questo modulo?",
    "Fornisci un riassunto della classe 'PaymentGatewayService'.",
]


# Funzione callback per i pulsanti di esempio.
# Essa inserisce la domanda direttamente nel campo di input principale
# e poi forza un rerun. Questo è l'approccio standard per gli esempi.
def handle_example_click(question_text):
    # Simula che l'utente abbia digitato questa domanda nel campo di input
    # st.session_state.messages.append({"role": "user", "content": question_text})
    # st.rerun.experimental_rerun() # Forza il rerun per innescare l'elaborazione dell'AI
    # st.session_state.user_input_value = question_text # Imposta il valore desiderato
    st.session_state.clicked_example_question = question_text


# Layout degli esempi su due colonne.
cols = st.columns(2)
for i, eq in enumerate(example_questions):
    with cols[i % 2]:
        st.button(eq, key=f"example_btn_{i}", on_click=handle_example_click, args=(eq,))

        # Questo blocco viene eseguito a ogni run dell'app.
# Controlla se una domanda d'esempio è stata "cliccata" nel run precedente
# e la processa se non è già stata processata.
if (
    "clicked_example_question" in st.session_state
    and st.session_state.clicked_example_question
):
    question_to_process = st.session_state.clicked_example_question
    # Pulisci subito per evitare elaborazioni duplicate in run futuri
    st.session_state.clicked_example_question = ""
    # Processa la domanda. Streamlit farà un rerun per mostrare la risposta.
    process_question(question_to_process)

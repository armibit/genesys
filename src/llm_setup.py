# src/llm_setup.py
import sys  #
import os  #

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(project_root)

from langchain_community.llms import Ollama
from langchain_community.llms import LlamaCpp
from config import LLM_MODEL_PATH


def bck_load_local_llm(n_gpu_layers=-1, n_batch=512, verbose=True):
    print("Connessione al modello LLM tramite Ollama...")
    try:
        # Crea un'istanza di Ollama. Assicurati che il nome del modello qui sia quello che hai scaricato con 'ollama pull'.
        # Ad esempio, 'codellama:7b-instruct' o 'deepseek-coder:7b-instruct'
        llm = Ollama(
            model="deepseek-r1:latest", temperature=0.7
        )  # Puoi specificare qui il modello scaricato
        print("Connessione a Ollama stabilita con successo!")
        return llm
    except Exception as e:
        print(
            f"Errore durante la connessione a Ollama o il caricamento del modello: {e}"
        )
        print(
            "Assicurati che il server Ollama sia in esecuzione e che il modello specificato sia scaricato."
        )
        raise


def load_local_llm(n_gpu_layers=-1, n_batch=512, verbose=True):
    """
    Carica un modello LLM locale in formato GGUF usando LlamaCpp.

    Args:
        n_gpu_layers (int): Numero di layer da scaricare sulla GPU (-1 per tutti i layer).
                            Imposta a 0 per eseguire solo su CPU.
        n_batch (int): Dimensione del batch per l'elaborazione.
        verbose (bool): Se mostrare l'output dettagliato di LlamaCpp.

    Returns:
        LlamaCpp: L'istanza del modello LLM caricato.
    """
    print(f"Tentativo di caricare il modello LLM da: {LLM_MODEL_PATH}")

    if not os.path.exists(LLM_MODEL_PATH):
        raise FileNotFoundError(
            f"Modello LLM non trovato al percorso specificato: {LLM_MODEL_PATH}. Assicurati di averlo scaricato e posizionato correttamente."
        )

    try:
        llm = LlamaCpp(
            model_path=LLM_MODEL_PATH,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            max_tokens=2048,  # Limita la lunghezza della risposta dell'LLM (opzionale)
            n_ctx=8192,  # Con 18GB di RAM, puoi tranquillamente usare 4096 o anche 8192 per modelli 7B
            verbose=verbose,
            n_threads=os.cpu_count(),  # Utilizza tutti i core logici disponibili
            temperature=0.7,  # Controllo della creatività (opzionale)
        )
        print("Modello LLM caricato con successo!")
        return llm
    except Exception as e:
        print(f"Errore durante il caricamento del modello LLM: {e}")
        print(
            "Assicurati che 'llama-cpp-python' sia installato correttamente (con supporto Metal per la tua GPU) e che il modello GGUF sia valido."
        )
        print(
            "Prova a impostare n_gpu_layers=0 per forzare l'esecuzione su CPU e verificare se il problema è la GPU."
        )
        raise


if __name__ == "__main__":
    # Importa os anche qui per usare os.cpu_count() nel test
    import os

    # Test del caricamento dell'LLM
    try:
        # Usa n_gpu_layers=-1 per sfruttare la GPU del tuo M3
        llm_model = load_local_llm(n_gpu_layers=-1)
        # Puoi fare una semplice query per testare
        print("\nTest query:")
        response = llm_model.invoke("Ciao, come stai? Descriviti brevemente.")
        print(response)
    except FileNotFoundError:
        print("Impossibile procedere senza il modello LLM. Scaricalo e riprova.")
    except Exception as e:
        print(
            f"Si è verificato un errore durante il test del caricamento dell'LLM: {e}"
        )

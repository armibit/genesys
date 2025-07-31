# Assistente AI per Codebase Java (Locale)

Questo progetto implementa un **assistente AI locale** in grado di rispondere a domande sulla codebase interna (Java, Spring Boot, API, database), utilizzando un approccio **RAG (Retrieval-Augmented Generation)**.  
L’obiettivo è fornire spiegazioni, analisi e snippet basati **esclusivamente sul codice sorgente indicizzato**.

---

## 🚀 Funzionalità Principali

- **Ricerca semantica nella codebase**: utilizza un database vettoriale (ChromaDB) per recuperare i file più rilevanti.
- **Risposte contestuali e sicure**: il modello non inventa risposte e si limita al perimetro del codice.
- **Supporto API & database**:
  - Analizza annotazioni (`@RestController`, `@GetMapping`, `@Entity`, `@Table`, ecc.)
  - Mostra path API, parametri richiesti, e tabelle collegate.
- **Interfaccia Streamlit**:
  - Chat con cronologia.
  - Possibilità di selezionare esempi di query.
  - Pulsante per resettare la cronologia.

---

## 🛠️ Struttura del Progetto

src/
├─ ingestion.py # Script per clonare repo, estrarre e indicizzare codice
├─ rag_pipeline.py # Classe CodeAssistant: gestisce retrieval + query al modello
├─ ui.py # Interfaccia Streamlit
├─ config.py # Configurazioni generali (modelli, path DB, ecc.)

---

## 📦 Tecnologie Utilizzate

- **LangChain** e **langchain-community**: pipeline RAG e splitter per codice (`CodeTextSplitter`).
- **ChromaDB**: database vettoriale locale.
- **HuggingFace Embeddings**: modelli embedding per indicizzare e ricercare codice.
- **Streamlit**: frontend semplice e interattivo.
- **Modelli LLM locali**: es. _Mistral-7B-Instruct_, _LLaMA 2_, o altri in formato **GGUF** via Ollama/llama.cpp.

---

## ▶️ Come Eseguire

1. **Clona il progetto** e crea l'ambiente virtuale:
   ```bash
   git clone <repo>
   cd code_assistant
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Ingestione del codice:**
3. bash
   Copia
   Modifica
   python src/ingestion.py
   Avvia l'interfaccia AI:

bash
Copia
Modifica
streamlit run src/ui.py
Fai una domanda:

Esempio: "Descrivi la funzione principale del metodo saveUser."

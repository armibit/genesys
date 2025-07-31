# src/rag_pipeline.py
import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

from config import CHROMA_DB_DIR, EMBEDDING_MODEL_NAME
from src.llm_setup import load_local_llm


class CodeAssistant:
    def __init__(self):
        print("Inizializzazione CodeAssistant...")
        # 1. Carica il modello di embedding
        # Ignoriamo il warning di deprecazione qui per il momento
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

        # 2. Carica il database vettoriale ChromaDB persistente
        try:
            self.vectorstore = Chroma(
                persist_directory=CHROMA_DB_DIR, embedding_function=self.embeddings
            )
            print(f"Database vettoriale caricato da {CHROMA_DB_DIR}")
        except Exception as e:
            print(f"Errore durante il caricamento di ChromaDB: {e}")
            print(
                "Assicurati che il database sia stato creato correttamente nella fase di ingestione."
            )
            raise

        # 3. Carica il modello LLM locale
        # n_gpu_layers=-1 è per il tuo Mac M3
        self.llm = load_local_llm(n_gpu_layers=-1)

        # 4. Definisci il template del prompt per la RAG
        # Questo template istruisce l'LLM su come rispondere
        # OLD: ChatPromptTemplate.from_messages([SystemMessage(content=(""))
        self.rag_prompt_template = ChatPromptTemplate.from_template(
            """
            [INST]
            Sei un assistente AI esperto in Java e architettura backend.

            Rispondi **solo** basandoti sul codice fornito nel CONTEXT.  
            Le risposte devono essere:

            - **Molto tecniche e dettagliate:** analizza annotazioni, validazioni, eccezioni, chiamate a repository, tabelle e colonne modificate.  
            - **Strutturate e formattate in Markdown:** con titoli, tabelle, elenco numerato e blocchi di codice se serve.  
            - **Complete:** non saltare nulla di importante.  
            - **Vincolate al contesto:** non inventare nulla, se manca un'informazione scrivi chiaramente che non è presente.  

            ---

            ### Quando la domanda riguarda un metodo:

            **1. Informazioni generali**

            - **Classe:** `NomeClasse` (in grassetto)  
            - **Metodo:** `NomeMetodo` (in grassetto)  
            - **Ruolo:** Controller, Service, Repository o altro  
            - **Endpoint HTTP (se API):**  
            - Path API (es. `@RequestMapping("/api/users")`)  
            - Metodo HTTP (es. `@GetMapping`, `POST`, ecc.)  

            **2. Parametri**

            | Tipo        | Nome      | Annotazioni              |
            |-------------|-----------|-------------------------|
            | DTO         | userDto   | @Valid, @RequestBody    |
            | PathVariable| id        | @PathVariable           |

            Descrivi la struttura completa del DTO di input (campi e tipo dati).

            **3. Logica interna del metodo**

            - Spiega in modo dettagliato ogni passo del flusso, indicando:  
            - Controlli eseguiti (es. validazioni, controlli nullità)  
            - Chiamate ad altri metodi o repository (es. `userRepository.save(user)`)  
            - Gestione delle eccezioni e errori previsti  
            - Validazioni con annotazioni o logica custom  

            **4. Persistenza e database**

            - Indica la/e tabella/e coinvolta/e  
            - Tipo di operazione (INSERT, UPDATE, DELETE, MERGE)  
            - Colonne o campi modificati o letti  
            - Query SQL o annotazioni JPA usate (es. `@Column`, `@Table`, query custom)  

            **5. Output**

            - Tipo restituito (es. `ResponseEntity<UserDto>`)  
            - Status HTTP previsto (es. `201 CREATED`)  
            - Descrizione e struttura del DTO di risposta  
            - Esempio realistico di JSON di output  

            ---

            ### Se mancano informazioni:

            Scrivi chiaramente:  
            _"Il contesto fornito non contiene abbastanza informazioni per rispondere in modo completo."_

            ---

            ### Requisiti di stile

            - Usa **grassetto** per classi, metodi, nomi di tabelle e annotazioni.  
            - Rispondi in sezioni chiare come sopra, con titoli Markdown.  
            - Non usare linguaggio generico o descrizioni astratte.  
            - Non omettere mai riferimenti a database o tabelle se presenti nel codice.  

            Rispondi nella lingua della domanda.

            Contesto:  
            {context}

            Domanda:  
            {question}
            [/INST]

            """
        )

        # 5. Crea la pipeline RAG
        # retriever: ricerca i chunk di codice più rilevanti nel DB vettoriale
        # format_docs: funzione per formattare i documenti recuperati nel prompt
        # chain: combina il retriever, il prompt e l'LLM
        self.rag_chain = (
            {
                "context": self.vectorstore.as_retriever(),
                "question": RunnablePassthrough(),
            }
            | self.rag_prompt_template
            | self.llm
            | StrOutputParser()
        )
        print("CodeAssistant inizializzato e pipeline RAG pronta.")

    def ask_codebase(self, question: str) -> str:
        """
        Interroga la codebase con una domanda usando la pipeline RAG.
        """
        print(f"\nDomanda: {question}")
        response = self.rag_chain.invoke(question)
        print("Risposta generata.")
        return response


if __name__ == "__main__":
    # Test della pipeline RAG
    try:
        assistant = CodeAssistant()

        # Esempi di domande. Adattale al tuo codice Java specifico!
        # Pensa a classi, metodi, concetti che sai essere presenti nel tuo repo.
        questions = [
            "Spiegami la classe 'UserService' e le sue funzionalità principali.",
            "Come viene gestita l'autenticazione nell'applicazione?",
            "Qual è lo scopo del metodo 'processOrder' nella classe 'OrderService'?",
            "Ci sono esempi di utilizzo di Spring Boot in questo codice?",
            "Descrivi il flusso di dati per la creazione di un nuovo utente.",
            "Dammi un esempio di utilizzo di un'interfaccia o di un'astrazione nel codice.",
            "Come vengono gestite le eccezioni comuni?",
            "Qual è la versione di Java usata o quali feature specifiche di Java vedo?",
            "Qual è la connessione al database e dove sono definite le credenziali?",
            "Spiegami questo pattern di design: [nome_pattern_se_presente_nel_tuo_codice]",  # Es: "Quale pattern di design è usato per le factory?"
        ]

        for i, q in enumerate(questions):
            print(f"\n--- Domanda {i+1} ---")
            print(f"Q: {q}")
            answer = assistant.ask_codebase(q)
            print(f"A: {answer}")
            print("\n" + "=" * 50 + "\n")

    except Exception as e:
        print(f"Errore durante l'esecuzione della pipeline RAG: {e}")

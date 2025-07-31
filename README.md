# Assistente AI per Codebase Java (Locale)

Un assistente intelligente per l'analisi e la comprensione di codebase Java, implementato con tecnologie RAG (Retrieval-Augmented Generation) per fornire risposte accurate e contestualizzate basate esclusivamente sul codice sorgente indicizzato.

---

## 📋 Panoramica del Progetto

Questo progetto implementa un **assistente AI locale** specializzato nell'analisi di codebase Java e Spring Boot. Utilizzando un approccio RAG (Retrieval-Augmented Generation), il sistema è in grado di:

- Analizzare e comprendere il codice sorgente Java
- Rispondere a domande specifiche sulla logica di business
- Fornire spiegazioni dettagliate su API, entità e relazioni database
- Mantenere la sicurezza dei dati processando tutto localmente

L'obiettivo principale è creare un assistente che fornisca **spiegazioni accurate, analisi approfondite e snippet di codice** basandosi esclusivamente sul codice sorgente indicizzato, senza inventare informazioni o fare assunzioni esterne.

---

## 🚀 Funzionalità Principali

### 🔍 Ricerca Semantica Avanzata

- **Database vettoriale locale**: utilizza ChromaDB per indicizzare e recuperare i frammenti di codice più rilevanti
- **Embedding semantici**: converte il codice in rappresentazioni vettoriali per ricerche intelligenti
- **Algoritmi di ranking**: ordina i risultati per rilevanza contestuale

### 🧠 Risposte Contestuali e Sicure

- **Limitazione al perimetro del codice**: il modello si basa esclusivamente sui file indicizzati
- **Prevenzione delle allucinazioni**: implementa controlli per evitare risposte inventate
- **Tracciabilità delle fonti**: ogni risposta è collegabile ai file sorgente specifici

### 🌐 Supporto Completo per Ecosistema Spring Boot

#### Analisi delle Annotazioni

- **Controller REST**: `@RestController`, `@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`
- **Gestione dati**: `@Entity`, `@Table`, `@Column`, `@JoinColumn`, `@OneToMany`, `@ManyToOne`
- **Configurazione**: `@Configuration`, `@Bean`, `@Component`, `@Service`, `@Repository`
- **Sicurezza**: `@PreAuthorize`, `@Secured`, `@RolesAllowed`

#### Mappatura API Completa

- **Endpoint discovery**: identificazione automatica di tutti gli endpoint REST
- **Analisi parametri**: tipo, validazione e obbligatorietà dei parametri
- **Response mapping**: struttura delle risposte e codici di stato
- **Relazioni database**: mapping tra entità e tabelle del database

### 💻 Interfaccia Utente Streamlit

#### Chat Interattiva

- **Cronologia conversazioni**: mantiene il contesto delle domande precedenti
- **Sintassi highlighting**: evidenziazione del codice nelle risposte
- **Copia rapida**: possibilità di copiare snippet di codice con un click

#### Query Predefinite

- **Esempi di utilizzo**: query template per casi d'uso comuni
- **Best practices**: suggerimenti per formulare domande efficaci
- **Shortcuts**: accesso rapido alle funzionalità più utilizzate

#### Gestione Sessioni

- **Reset cronologia**: pulsante per iniziare una nuova sessione
- **Esportazione conversazioni**: salvataggio delle chat in formato markdown
- **Configurazioni personalizzate**: adattamento dell'interfaccia alle preferenze utente

---

## 🛠️ Architettura del Sistema

### Struttura del Progetto

```
src/
├── ingestion.py          # Modulo per l'acquisizione e indicizzazione del codice
├── rag_pipeline.py       # Pipeline RAG e classe CodeAssistant principale
├── ui.py                 # Interfaccia utente Streamlit
├── config.py            # Configurazioni di sistema e parametri
├── utils/
│   ├── code_parser.py   # Parser specializzati per Java/Spring Boot
│   ├── embeddings.py    # Gestione embedding e similarità
│   └── validators.py    # Validatori per query e risposte
└── tests/
    ├── test_ingestion.py
    ├── test_rag.py
    └── test_ui.py
```

### Flusso di Elaborazione

#### 1. Fase di Ingestione (`ingestion.py`)

```python
# Pseudocodice del processo di ingestione
def ingest_codebase():
    # Clone del repository
    repo = clone_repository(repo_url)

    # Estrazione file Java
    java_files = extract_java_files(repo)

    # Parsing e chunking intelligente
    chunks = []
    for file in java_files:
        parsed = parse_java_file(file)
        chunks.extend(smart_chunk_code(parsed))

    # Generazione embedding
    embeddings = generate_embeddings(chunks)

    # Indicizzazione in ChromaDB
    store_in_vector_db(chunks, embeddings)
```

#### 2. Pipeline RAG (`rag_pipeline.py`)

```python
class CodeAssistant:
    def __init__(self):
        self.vector_db = ChromaDB()
        self.llm = load_local_model()
        self.embeddings = HuggingFaceEmbeddings()

    def query(self, question):
        # Retrieval fase
        relevant_chunks = self.vector_db.similarity_search(question)

        # Augmentation fase
        context = build_context(relevant_chunks)

        # Generation fase
        response = self.llm.generate(question, context)

        return response, relevant_chunks
```

---

## 📦 Stack Tecnologico

### Framework e Librerie Core

#### LangChain Ecosystem

- **LangChain Core** (`v0.1.52`): Framework principale per applicazioni LLM
- **LangChain Community** (`v0.0.38`): Integrazioni con tool esterni
- **CodeTextSplitter**: Splitter specializzato per linguaggi di programmazione
- **Document Loaders**: Caricamento efficiente di file sorgente

#### Database Vettoriale

- **ChromaDB** (`v0.4.24`): Database vettoriale open-source
  - Indicizzazione locale ad alte prestazioni
  - Supporto per metadati complessi
  - Query semantiche avanzate
  - Persistenza su disco

#### Modelli di Embedding

- **HuggingFace Transformers**: Modelli pre-addestrati per embedding
  - `all-MiniLM-L6-v2`: Bilanciamento prestazioni/qualità
  - `code-search-net`: Specializzato per codice sorgente
  - `multilingual-e5-large`: Supporto multilingua

#### Interfaccia Utente

- **Streamlit** (`v1.28.1`): Framework per applicazioni web interattive
  - Componenti reattivi per chat
  - Gestione stato sessioni
  - Deploy semplificato

### Modelli LLM Supportati

#### Modelli Locali (Raccomandati)

- **Mistral-7B-Instruct**: Eccellente per reasoning su codice
- **CodeLlama-7B-Instruct**: Specializzato per programmazione
- **LLaMA 2-7B-Chat**: Versatile per conversazioni tecniche
- **DeepSeek-Coder-6.7B**: Ottimizzato per analisi codice

#### Runtime Supportati

- **Ollama**: Gestione semplice modelli locali
- **llama.cpp**: Inferenza efficiente CPU
- **HuggingFace Transformers**: Integrazione diretta Python

---

## ⚙️ Configurazione e Installazione

### Prerequisiti di Sistema

- **Python 3.8+** (raccomandato 3.10+)
- **Git** per clonazione repository
- **8GB RAM** minimo (16GB raccomandato)
- **10GB spazio disco** per modelli e database

### Installazione Dettagliata

#### 1. Setup Ambiente

```bash
# Clone del repository
git clone https://github.com/your-org/java-ai-assistant.git
cd java-ai-assistant

# Creazione ambiente virtuale
python -m venv venv

# Attivazione ambiente (Linux/Mac)
source venv/bin/activate
# Attivazione ambiente (Windows)
venv\Scripts\activate

# Installazione dipendenze
pip install -r requirements.txt
```

#### 2. Configurazione Modelli

```bash
# Installazione Ollama (opzionale)
curl -fsSL https://ollama.ai/install.sh | sh

# Download modello raccomandato
ollama pull mistral:7b-instruct

# Verifica installazione
ollama list
```

#### 3. Configurazione Parametri

```python
# config.py - Configurazioni principali
class Config:
    # Database vettoriale
    CHROMA_DB_PATH = "./data/chroma_db"
    COLLECTION_NAME = "java_codebase"

    # Modello LLM
    MODEL_NAME = "mistral:7b-instruct"
    MODEL_TEMPERATURE = 0.1
    MAX_TOKENS = 2048

    # Embedding
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # Repository
    REPO_URL = "https://github.com/your-org/java-project.git"
    SUPPORTED_EXTENSIONS = [".java", ".xml", ".properties", ".yml"]
```

---

## ▶️ Guida all'Utilizzo

### Avvio Rapido

#### 1. Indicizzazione Codebase

```bash
# Esecuzione ingestione completa
python src/ingestion.py --repo-url https://github.com/your-org/project.git

# Opzioni avanzate
python src/ingestion.py \
    --repo-url https://github.com/your-org/project.git \
    --branch main \
    --include-tests \
    --chunk-size 1500 \
    --max-files 1000
```

#### 2. Avvio Interfaccia

```bash
# Lancio applicazione Streamlit
streamlit run src/ui.py

# Con configurazioni personalizzate
streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0
```

#### 3. Utilizzo Base

```
🌐 Aprire: http://localhost:8501
💬 Digitare domanda nella chat
🔍 Visualizzare risultati con sorgenti
```

### Esempi di Query Avanzate

#### Analisi API REST

```
Query: "Elenca tutti gli endpoint GET che restituiscono dati utente"
Risposta: Identificazione automatica di:
- Controller coinvolti
- Path mapping completi
- Parametri richiesti/opzionali
- Struttura response DTO
- Validazioni applicate
```

#### Mappatura Database

```
Query: "Descrivi la relazione tra User e Order entities"
Risposta: Analisi di:
- Annotazioni JPA
- Chiavi primarie/esterne
- Strategie di fetch
- Cascade operations
- Indici database
```

#### Logica Business

```
Query: "Come funziona il processo di validazione in UserService?"
Risposta: Spiegazione di:
- Flusso metodi validazione
- Regole business implementate
- Gestione eccezioni
- Dipendenze esterne
```

### Query Templates Integrate

L'interfaccia include template predefiniti per casi d'uso comuni:

#### 🔧 Analisi Architetturale

- "Mostra la struttura dei package e le dipendenze principali"
- "Identifica i design pattern utilizzati nel progetto"
- "Analizza la configurazione Spring Boot"

#### 🌐 API e Endpoint

- "Lista tutti gli endpoint REST con i loro metodi HTTP"
- "Trova API che utilizzano validazione Bean Validation"
- "Mostra endpoint che richiedono autenticazione"

#### 🗄️ Database e Persistenza

- "Descrivi lo schema del database dalle entity JPA"
- "Trova query native SQL nel codice"
- "Analizza le relazioni tra tabelle"

#### 🧪 Testing e Qualità

- "Mostra la copertura dei test per ogni service"
- "Identifica metodi senza test unitari"
- "Analizza i mock utilizzati nei test"

---

## 🔧 Configurazioni Avanzate

### Ottimizzazione Performance

```python
# Configurazioni per dataset grandi
class PerformanceConfig:
    # Chunking intelligente
    CHUNK_SIZE = 1500
    CHUNK_OVERLAP = 300
    MAX_CHUNKS_PER_FILE = 50

    # Retrieval ottimizzato
    SIMILARITY_THRESHOLD = 0.7
    MAX_RELEVANT_CHUNKS = 10
    RERANK_TOP_K = 20

    # Caching
    ENABLE_RESPONSE_CACHE = True
    CACHE_TTL_SECONDS = 3600
    MAX_CACHE_SIZE = 1000
```

---

## 🚀 Deployment e Produzione

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Installazione dipendenze sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installazione Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copia applicazione
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

# Esponi porta Streamlit
EXPOSE 8501

# Script di avvio
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
```

```bash
# start.sh
#!/bin/bash
set -e

# Avvio Ollama in background
ollama serve &

# Attesa per inizializzazione Ollama
sleep 10

# Download modello se non presente
ollama list | grep -q mistral || ollama pull mistral:7b-instruct

# Avvio applicazione Streamlit
streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🔍 Troubleshooting e FAQ

### Problemi Comuni e Soluzioni

#### Memory Issues

```
Problema: "Out of memory durante l'embedding generation"
Soluzione:
- Ridurre CHUNK_SIZE in config.py
- Processare file in batch più piccoli
- Aumentare swap sistema
- Usare modelli embedding più leggeri
```

#### Performance Lente

```
Problema: "Query molto lente (>30 secondi)"
Soluzioni:
- Ottimizzare threshold similarità
- Ridurre MAX_RELEVANT_CHUNKS
- Abilitare caching risposte
- Usare SSD per ChromaDB
- Considerare GPU per inferenza
```

#### Risposte Incomplete

```
Problema: "L'assistente non trova codice rilevante"
Soluzioni:
- Verificare indicizzazione completa
- Ridurre SIMILARITY_THRESHOLD
- Migliorare formulazione query
- Aggiornare embedding con nuovo codice
```

### FAQ Dettagliate

**Q: Posso usare l'assistente con codice Kotlin o Scala?**
A: Attualmente ottimizzato per Java/Spring Boot, ma estendibile modificando i parser in `code_parser.py` per supportare altri linguaggi JVM.

**Q: Come aggiorno l'indice quando il codice cambia?**
A: Eseguire `python src/ingestion.py --incremental` per aggiornamento rapido, o `--full-reindex` per ricostruzione completa.

**Q: L'assistente può suggerire refactoring?**
A: Sì, può identificare code smells, pattern duplicati e suggerire miglioramenti basandosi sulle best practices riconosciute nel codice esistente.

**Q: È possibile integrare con IDE come IntelliJ?**
A: Pianificato per versioni future. Attualmente disponibile plugin VS Code basic tramite API REST.

---

## 🛣️ Roadmap e Sviluppi Futuri

### Versione 1.0 (Q3 2025)

- **Multi-repository support**: Analisi di più progetti contemporaneamente
- **Advanced code metrics**: Calcolo complessità ciclomatica, technical debt
- **Interactive code visualization**: Grafici di dipendenze e architettura
- **Custom prompt templates**: Template personalizzabili per domini specifici

### Versione 2.0 (Q4 2025)

- **Integration testing analysis**: Comprensione test di integrazione
- **Performance profiling**: Identificazione colli di bottiglia nel codice
- **Security analysis**: Rilevamento vulnerabilità e best practices sicurezza
- **Migration assistant**: Supporto per upgrade framework e versioni

### Versione 3.0 (Q1 2026)

- **Real-time collaboration**: Condivisione sessioni tra team members
- **Advanced reasoning**: Capacità di reasoning su logica business complessa
- **Auto-documentation**: Generazione automatica documentazione tecnica

---

## 🤝 Contribuire al Progetto

### Guidelines per Contributori

#### Setup Ambiente Sviluppo

```bash
# Fork e clone
git clone https://github.com/your-username/java-ai-assistant.git
cd java-ai-assistant

# Installazione dipendenze sviluppo
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Esecuzione test
pytest tests/ -v --cov=src/
```

#### Tipi di Contributi Benvenuti

- **Bug fixes**: Correzione problemi identificati
- **Feature development**: Implementazione nuove funzionalità
- **Documentation**: Miglioramento documentazione e tutorial
- **Testing**: Aggiunta test coverage e casi edge
- **Performance**: Ottimizzazioni algoritmi e memoria
- **Integration**: Supporto nuovi modelli LLM e framework

#### Process di Review

1. **Issue creation**: Descrizione dettagliata problema/feature
2. **Branch development**: Feature branch con naming convention
3. **Code review**: Peer review obbligatorio prima merge
4. **Testing**: Tutti i test devono passare
5. **Documentation update**: Aggiornamento docs se necessario

---

## 📄 Licenza e Riconoscimenti

### Licenza

Questo progetto è rilasciato sotto licenza **MIT License**. Vedi il file `LICENSE` per dettagli completi.

### Riconoscimenti e Credits

- **LangChain Team**: Framework RAG e integrazioni LLM
- **ChromaDB**: Database vettoriale open-source performante
- **HuggingFace**: Modelli pre-addestrati e ecosystem AI
- **Streamlit**: Framework per rapid prototyping UI
- **Ollama Team**: Runtime semplificato per modelli locali

---

_Ultima modifica: Luglio 2025_
_Versione documentazione: 1.2.0_

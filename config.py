# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPOS_DIR = os.path.join(DATA_DIR, "repos")
CHROMA_DB_DIR = os.path.join(DATA_DIR, "db")
MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(REPOS_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# --- Configurazione del Repository di Test ---
# Puoi cambiare questo URL con un tuo repository pubblico di test
GITHUB_REPO_URL = ""  # Esempio di un piccolo repo Python
REPO_NAME = GITHUB_REPO_URL.split("/")[-1].replace(".git", "")

# --- Configurazione Embeddings ---
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# --- Configurazione LLM Locale (per la Fase 3) ---
LLM_MODEL_NAME = "mistral-7b-instruct-v0.2.Q5_K_S.gguf"
LLM_MODEL_PATH = os.path.join(MODELS_DIR, LLM_MODEL_NAME)

# --- Impostazioni per il Chunking del Codice ---
CHUNK_SIZE = 1000  # Dimensione massima dei "pezzi" di codice (in caratteri)
CHUNK_OVERLAP = 400  # Sovrapposizione tra i pezzi per mantenere il contesto

# --- Bitbucket Credentials (se necessarie in futuro) ---
BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME")
BITBUCKET_APP_PASSWORD = os.getenv("BITBUCKET_APP_PASSWORD")

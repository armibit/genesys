# src/ingestion.py

import sys  #
import os  #

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(project_root)

import warnings
import logging

warnings.filterwarnings("ignore", message=".*libmagic.*")
logging.getLogger("langchain").setLevel(logging.ERROR)

import shutil
import json
import javalang
import shutil
from git import Repo, GitCommandError
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import (
    REPOS_DIR,
    CHROMA_DB_DIR,
    GITHUB_REPO_URL,
    REPO_NAME,
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def clone_repository(repo_url: str, local_path: str):
    """
    Clona un repository Git o aggiorna se esiste già.
    """
    print(f"Tentativo di clonare/aggiornare il repository: {repo_url}")
    if os.path.exists(local_path):
        print(f"Repository {local_path} esiste già. Aggiornamento in corso...")
        try:
            repo = Repo(local_path)
            origin = repo.remotes.origin
            origin.pull()
            print("Repository aggiornato con successo.")
        except GitCommandError as e:
            print(f"Errore durante l'aggiornamento del repository: {e}")
            # Potrebbe essere un repository corrotto, tentiamo di riclonare
            print(f"Elimino e riclono {local_path}...")
            shutil.rmtree(local_path)
            Repo.clone_from(repo_url, local_path)
            print("Repository riclonato con successo.")
        except Exception as e:
            print(f"Errore inatteso durante l'aggiornamento: {e}")
            print(f"Elimino e riclono {local_path}...")
            shutil.rmtree(local_path)
            Repo.clone_from(repo_url, local_path)
            print("Repository riclonato con successo.")
    else:
        print(f"Clonazione del repository in {local_path}...")
        try:
            Repo.clone_from(repo_url, local_path)
            print("Repository clonato con successo.")
        except GitCommandError as e:
            print(f"Errore durante la clonazione del repository: {e}")
            raise


def load_and_split_code(repo_path: str):
    """
    Carica i file di codice e li divide in chunk.
    Ignora i file binari e le cartelle .git.
    """
    print(f"Caricamento e suddivisione dei file di codice da {repo_path}...")
    # Loader per tutti i tipi di testo comuni, escludendo alcuni binari e .git
    loader = DirectoryLoader(
        repo_path,
        glob="**/*",  # Carica tutti i file
        # loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True},
        exclude=[
            "**/.*",
            "**/*.bin",
            "**/*.log",
            "**/*.sqlite3",
            "**/*.db",
            "**/*.DS_Store",
            "**/*.pyc",
            "**/*.lock",
            "**/node_modules/**",
            "**/venv/**",
            "**/*.jar",
            "**/*.class",
            "**/*.zip",
            "**/*.tar",
            "**/*.gz",
            "**/*.rar",
            "**/*.7z",
            "**/*.jpg",
            "**/*.jpeg",
            "**/*.png",
            "**/*.gif",
            "**/*.bmp",
            "**/*.ico",
            "**/*.svg",
            "**/*.pdf",
            "**/*.doc",
            "**/*.docx",
            "**/*.xls",
            "**/*.xlsx",
            "**/*.ppt",
            "**/*.pptx",
            "**/*.mp3",
            "**/*.wav",
            "**/*.mp4",
            "**/*.avi",
            "**/*.mov",
            "**/*.dll",
            "**/*.exe",
            "**/*.so",
            "**/*.dylib",
            "**/*.o",
            "**/*.a",
            "**/*.p12",
            "**/*.pem",
            "**/*.crt",
            "**/*.key",
            "**/*.jks",
            "**/node_modules/**",
            "**/venv/**",
            "**/target/**",
            "**/build/**",
            "**/dist/**",
            "**/test-results/**",
            "**/tmp/**",
            "**/logs/**",
            "**/out/**",
            "**/gen/**",
            "**/target/**",
            "**/build/**",
            "**/.git/**",
        ],
        show_progress=True,
    )
    documents = loader.load()

    print(f"Trovati {len(documents)} documenti.")

    # Inizializza lo splitter per il testo
    # RecursiveCharacterTextSplitter è ottimo per il codice perché prova a dividere per caratteri
    # e poi per linea, poi per spazio, ecc., mantenendo il contesto.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        # is_separator_regex=False,  # Non usare regex per i separatori di default
        # language=Language.JAVA,
    )
    # Potresti voler personalizzare i separatori per il codice, es:
    # separators=["\n\n", "\n", " ", ""]
    # Per ora, quelli di default di RecursiveCharacterTextSplitter sono un buon inizio.

    chunks = text_splitter.split_documents(documents)
    print(f"Suddivisi in {len(chunks)} chunk di codice.")
    return chunks


def extract_method_text(java_code: str, method_node, class_name: str):
    """Estrae il testo di un singolo metodo dal codice Java."""
    lines = java_code.split("\n")

    # Trova la linea di inizio del metodo
    start_line = method_node.position.line - 1  # javalang usa 1-based indexing

    # Trova la fine del metodo cercando le parentesi graffe bilanciate
    brace_count = 0
    end_line = start_line
    found_opening_brace = False

    for i in range(start_line, len(lines)):
        line = lines[i]
        for char in line:
            if char == "{":
                brace_count += 1
                found_opening_brace = True
            elif char == "}":
                brace_count -= 1
                if found_opening_brace and brace_count == 0:
                    end_line = i
                    break
        if found_opening_brace and brace_count == 0:
            break

    # Estrae le linee del metodo
    method_lines = lines[start_line : end_line + 1]
    return "\n".join(method_lines)


def load_and_analyze_code(repo_path: str):
    print(f"Caricamento e analisi del codice da {repo_path}...")
    loader = DirectoryLoader(
        repo_path,
        glob="**/*.java",
        loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True},
        exclude=["**/target/**", "**/build/**", "**/.git/**"],
        show_progress=True,
    )
    raw_docs = loader.load()
    # da controllare se funziona
    documents = [
        (
            d
            if isinstance(d, Document)
            else Document(
                page_content=d.get("text", ""), metadata=d.get("metadata", {})
            )
        )
        for d in raw_docs
    ]
    print(f"Trovati {len(documents)} file Java.")

    enriched_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    for doc in documents:
        file_path = doc.metadata["source"]
        java_code = doc.page_content

        # Estraggo AST e metadati
        methods_info = extract_java_structure(java_code, file_path)
        if not methods_info:
            # fallback: normale chunk
            for chunk in splitter.split_text(java_code):
                if len(chunk.strip()) > 30:  # ✅ Evita chunk inutili
                    enriched_chunks.append(
                        Document(page_content=chunk, metadata={"file": file_path})
                    )
        else:
            for m in methods_info:
                if len(m["text"].strip()) > 30:
                    enriched_chunks.append(
                        Document(
                            page_content=m["text"],
                            metadata={
                                "file": m["file"],
                                "class": m["class"],
                                "method": m["method"],
                                "calls": ", ".join(m["calls"]) if m["calls"] else "",
                                "params": ", ".join(m["params"]) if m["params"] else "",
                                "param_names": (
                                    ", ".join(m["param_names"])
                                    if m["param_names"]
                                    else ""
                                ),
                                "return_type": m["return_type"],
                                "modifiers": (
                                    ", ".join(m["modifiers"]) if m["modifiers"] else ""
                                ),
                                "variables": (
                                    ", ".join(m["variables"]) if m["variables"] else ""
                                ),
                                "num_params": len(m["params"]) if m["params"] else 0,
                                "num_calls": len(m["calls"]) if m["calls"] else 0,
                                "method_signature": f"{m['class']}.{m['method']}({', '.join(m['params']) if m['params'] else ''})",
                                "content_type": "java_method",
                            },
                        )
                    )
    print(f"Generati {len(enriched_chunks)} chunk con metadati.")
    return enriched_chunks


def create_vector_db(chunks, db_path: str, embedding_model_name: str):
    """
    Crea o aggiorna il database vettoriale ChromaDB con i chunk di codice.
    """
    print(f"Creazione/aggiornamento del database vettoriale in {db_path}...")
    # Debug: verifica che tutti gli elementi siano Document
    print(f"Tipo del primo chunk: {type(chunks[0])}")
    if hasattr(chunks[0], "page_content"):
        print("✓ Gli oggetti hanno l'attributo page_content")
    else:
        print("✗ Gli oggetti NON hanno l'attributo page_content")
        # Converti i dizionari in Document se necessario
        converted_chunks = []
        for chunk in chunks:
            if isinstance(chunk, dict):
                converted_chunks.append(
                    Document(
                        page_content=chunk.get("text", ""),
                        metadata=chunk.get("metadata", {}),
                    )
                )
            else:
                converted_chunks.append(chunk)
        chunks = converted_chunks
    # Inizializza il modello di embedding
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    # Crea o carica il database ChromaDB
    # 'persist_directory' specifica dove salvare il database su disco
    vector_db = Chroma.from_documents(chunks, embeddings, persist_directory=db_path)
    vector_db.persist()  # Salva il database su disco
    print("Database vettoriale creato/aggiornato con successo.")
    return vector_db


def extract_java_structure(java_code: str, file_path: str):
    """Estrae classi, metodi e call graph da un file Java."""
    try:
        tree = javalang.parse.parse(java_code)
    except Exception:
        return []

    data = []

    for _, class_decl in tree.filter(javalang.tree.ClassDeclaration):
        for method in class_decl.methods:
            called_methods = []
            used_variables = []
            if method.body:
                for path, node in method:
                    if isinstance(node, javalang.tree.MethodInvocation):
                        called_methods.append(node.member)
                    elif isinstance(node, javalang.tree.MemberReference):
                        used_variables.append(node.member)
            try:
                method_text = extract_method_text(java_code, method, class_decl.name)
            except Exception as e:
                print(
                    f"Errore nell'estrazione del metodo {method.name} da {file_path}: {e}"
                )
                # Fallback: usa tutto il file se non riesco a estrarre il metodo
                method_text = java_code

            # Estrai informazioni aggiuntive dal metodo
            param_types = (
                [p.type.name for p in method.parameters] if method.parameters else []
            )
            param_names = (
                [p.name for p in method.parameters] if method.parameters else []
            )
            return_type = method.return_type.name if method.return_type else "void"
            modifiers = method.modifiers if method.modifiers else []

            data.append(
                {
                    "class": class_decl.name,
                    "method": method.name,
                    "params": param_types,
                    "param_names": param_names,
                    "return_type": return_type,
                    "modifiers": modifiers,
                    "calls": called_methods,
                    "variables": used_variables,
                    "file": file_path,
                    "text": method_text,
                }
            )
    return data


if __name__ == "__main__":
    # Percorso dove verrà clonato il repository
    local_repo_path = os.path.join(REPOS_DIR, REPO_NAME)

    # 1. Clona o aggiorna il repository
    clone_repository(GITHUB_REPO_URL, local_repo_path)

    # 2. Carica e suddividi il codice in chunk
    # code_chunks = load_and_split_code(local_repo_path)
    code_chunks = load_and_analyze_code(local_repo_path)

    # 3. Crea il database vettoriale
    # ChromaDB salverà i dati nella directory specificata da CHROMA_DB_DIR
    vector_database = create_vector_db(code_chunks, CHROMA_DB_DIR, EMBEDDING_MODEL_NAME)

    print("\n✅ Processo di ingestione completato!")
    print(f"📌 Il database vettoriale è salvato in: {CHROMA_DB_DIR}")
    print(f"🔢 Contiene {vector_database._collection.count()} elementi.")

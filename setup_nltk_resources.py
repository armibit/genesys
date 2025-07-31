import nltk
import ssl
import os
import urllib.request


# Soluzione completa per problemi SSL (comune su macOS)
def fix_ssl_context():
    """Fix SSL context per NLTK downloads"""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python che non ha ssl._create_unverified_context
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Configurazione aggiuntiva per urllib
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Installa il nuovo contesto
    urllib.request.install_opener(
        urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    )


# Applica la fix SSL
fix_ssl_context()

# Imposta la directory di download (opzionale)
# nltk.data.path.append('/path/to/your/nltk_data')

resources = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "wordnet",
    "omw-1.4",
    "averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng",
]


def download_nltk_resources():
    """Scarica le risorse NLTK con gestione errori migliorata"""

    print("Inizio download risorse NLTK...")

    # Mostra informazioni directory NLTK
    try:
        data_path = nltk.data.path[0]
        print(f"Directory NLTK data: {data_path}")
    except:
        print("Directory NLTK data: non determinabile")

    success_count = 0
    failed_resources = []

    for resource in resources:
        try:
            print(f"\nScaricando '{resource}'...")

            # Verifica se la risorsa è già presente e funzionante
            is_present = False
            resource_paths = [
                f"tokenizers/{resource}",
                f"corpora/{resource}",
                f"taggers/{resource}",
                f"chunkers/{resource}",
                f"models/{resource}",
            ]

            for path in resource_paths:
                try:
                    nltk.data.find(path)
                    print(f"Risorsa '{resource}' già presente e accessibile.")
                    is_present = True
                    success_count += 1
                    break
                except LookupError:
                    continue

            if is_present:
                continue

            # Scarica la risorsa con retry
            print(f"Tentativo download di '{resource}'...")

            # Primo tentativo
            try:
                result = nltk.download(resource, quiet=False, force=False)
                if result:
                    print(f"✓ Risorsa '{resource}' scaricata con successo.")
                    success_count += 1
                else:
                    # Secondo tentativo con force=True
                    print(f"Retry download di '{resource}' con force=True...")
                    result = nltk.download(resource, quiet=False, force=True)
                    if result:
                        print(f"✓ Risorsa '{resource}' scaricata con successo (retry).")
                        success_count += 1
                    else:
                        print(f"✗ Download fallito per '{resource}'")
                        failed_resources.append(resource)
            except Exception as download_error:
                print(f"✗ Errore durante download di '{resource}': {download_error}")
                failed_resources.append(resource)

        except Exception as e:
            print(f"✗ Errore generale per '{resource}': {type(e).__name__}: {e}")
            failed_resources.append(resource)

    # Riepilogo
    print(f"\n{'='*50}")
    print(f"RIEPILOGO DOWNLOAD:")
    print(f"Risorse scaricate con successo: {success_count}/{len(resources)}")

    if failed_resources:
        print(f"Risorse fallite: {failed_resources}")
        print("\nSuggerimenti per risolvere i problemi:")
        print("1. Verifica la connessione internet")
        print("2. Prova a eseguire come amministratore/sudo")
        print("3. Controlla i permessi della directory NLTK")
        print("4. Prova a scaricare manualmente: nltk.download()")
    else:
        print("Tutte le risorse sono state scaricate correttamente!")


def test_resources():
    """Testa se le risorse sono utilizzabili"""
    print(f"\n{'='*50}")
    print("TEST DELLE RISORSE:")

    try:
        # Test punkt
        from nltk.tokenize import sent_tokenize, word_tokenize

        test_text = "Ciao mondo. Come stai?"
        sentences = sent_tokenize(test_text)
        words = word_tokenize(test_text)
        print("✓ punkt: OK")
    except Exception as e:
        print(f"✗ punkt: {e}")

    try:
        # Test stopwords
        from nltk.corpus import stopwords

        stop_words = stopwords.words("english")
        print("✓ stopwords: OK")
    except Exception as e:
        print(f"✗ stopwords: {e}")

    try:
        # Test wordnet
        from nltk.corpus import wordnet

        syns = wordnet.synsets("good")
        print("✓ wordnet: OK")
    except Exception as e:
        print(f"✗ wordnet: {e}")

    try:
        # Test tagger
        from nltk import pos_tag
        from nltk.tokenize import word_tokenize

        text = "This is a test"
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        print("✓ averaged_perceptron_tagger: OK")
    except Exception as e:
        print(f"✗ averaged_perceptron_tagger: {e}")


if __name__ == "__main__":
    # Scarica le risorse
    download_nltk_resources()

    # Testa le risorse
    test_resources()

    print(f"\n{'='*50}")
    print("Script completato!")

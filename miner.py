from pydriller import Repository

# Questa funzione serve a trovare i commit che correggono bug
def analyze_repo(repo_url):
    print(f"🔄 Inizio analisi su: {repo_url}...")
    
    # Lista dove salveremo i risultati
    bug_fixing_commits = []
    
    # Repository(...) scarica la repo ed estrae la storia
    # traverse_commits() è un ciclo che legge i commit uno per uno, dal più vecchio al più nuovo
    # Usiamo 'only_in_branch="main"' o "master" solitamente, ma per ora va bene default
    for commit in Repository(repo_url).traverse_commits():
        
        # 1. IL FILTRO: Cerchiamo parole chiave nel messaggio del commit
        msg = commit.msg.lower() # Convertiamo in minuscolo per non sbagliare
        if "fix" in msg or "bug" in msg or "resolve" in msg:
            
            print(f"  Found Fix: {commit.hash[:7]} - {commit.msg.splitlines()[0]}")
            
            # 2. ESTRAZIONE DATI: Guardiamo i file toccati in questo commit
            for modified_file in commit.modified_files:
                
                # Ci interessano solo i file Python (.py) per questo progetto
                if modified_file.filename.endswith(".py"):
                    
                    # Salviamo i dati che servono all'LLM
                    candidate = {
                        "commit_hash": commit.hash,
                        "author": commit.author.name,
                        "date": commit.committer_date,
                        "message": commit.msg,
                        "filename": modified_file.filename,
                        "diff": modified_file.diff # <--- Questo è il codice cambiato!
                    }
                    bug_fixing_commits.append(candidate)
        
        # STOP DI SICUREZZA: Per ora fermiamoci dopo averne trovati 5
        # (altrimenti su repo grandi ci mette ore)
        if len(bug_fixing_commits) >= 5:
            break
            
    print(f"✅ Analisi finita. Trovati {len(bug_fixing_commits)} potenziali fix.")
    return bug_fixing_commits

# Questo pezzo serve per testare lo script da solo
if __name__ == "__main__":
    # Usiamo una repo di test piccola (requests è famosa)
    test_url = "https://github.com/psf/requests"
    
    risultati = analyze_repo(test_url)
    
    # Stampiamo il primo risultato per vedere com'è fatto
    if risultati:
        print("\n--- DETTAGLIO PRIMO RISULTATO ---")
        print(f"File: {risultati[0]['filename']}")
        print(f"Diff (Prime 5 righe):\n{risultati[0]['diff'][:200]}...")
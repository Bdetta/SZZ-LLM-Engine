import miner
import analyzer
import json

# Configurazione
REPO_URL = "https://github.com/psf/requests" # Usiamo questa per testare

def main():
    print(f"🚀 Avvio SZZ Engine su {REPO_URL}...")
    
    # 1. FASE MINING (Membro A)
    commits = miner.analyze_repo(REPO_URL)
    print(f"📊 Trovati {len(commits)} commit candidati.")
    
    results = []
    
    # 2. FASE ANALISI (Membro B)
    for commit in commits:
        print(f"\n🔍 Analisi commit: {commit['commit_hash'][:7]}")
        
        # Chiediamo all'IA
        llm_response = analyzer.analyze_commit(commit['message'], commit['diff'])
        
        # Salviamo il risultato
        results.append({
            "hash": commit['commit_hash'],
            "msg": commit['message'],
            "llm_verdict": llm_response
        })

    # 3. SALVATAGGIO REPORT
    with open("final_report.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\n✅ Finito! Report salvato in 'final_report.json'")

if __name__ == "__main__":
    main()
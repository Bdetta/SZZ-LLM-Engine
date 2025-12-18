import os
from openai import OpenAI
from dotenv import load_dotenv

# Carica la chiave dal file .env
load_dotenv()

# Configura il client OpenAI
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Errore configurazione API Key: {e}")

def analyze_commit(message, diff):
    """
    Funzione che chiede all'LLM se un commit è un vero bug fix.
    """
    print("⏳ Chiedo all'IA...")
    
    prompt = f"""
    Analizza questo commit Git.
    Messaggio: "{message}"
    Diff (Modifiche):
    {diff}
    
    Domanda: Questo commit risolve un bug logico nel codice?
    Rispondi con un JSON: {{"is_bug_fix": true/false, "reason": "breve spiegazione"}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Errore durante la chiamata API: {e}"

# --- TEST LOCALE ---
if __name__ == "__main__":
    # Testiamo con dati finti per vedere se funziona
    fake_msg = "Fixed division by zero"
    fake_diff = "+ if b == 0: return 0\n+ return a / b"
    
    risultato = analyze_commit(fake_msg, fake_diff)
    print("\n--- RISULTATO ---")
    print(risultato)
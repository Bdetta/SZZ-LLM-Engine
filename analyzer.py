import os
from openai import OpenAI # Usiamo la stessa libreria!
from dotenv import load_dotenv

# Carica le variabili (non serve più la chiave, ma lasciamo il caricamento)
load_dotenv()

# --- MODIFICA FONDAMENTALE PER OLLAMA ---
# Invece di collegarsi a internet, ci colleghiamo al tuo PC
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Indirizzo di Ollama
    api_key="ollama",                      # Chiave finta (obbligatoria ma ignorata)
)

def analyze_commit(message, diff):
    print("⏳ Chiedo a Qwen (Locale)...") # Ho cambiato il testo per chiarezza
    
    # Prompt ottimizzato per modelli locali
    prompt = f"""
    Sei un esperto di Software Engineering. Analizza il seguente commit.
    
    Commit Message: "{message}"
    
    Diff:
    {diff}
    
    Compito: Il commit risolve un bug?
    Rispondi SOLO in formato JSON valido:
    {{
        "is_bug_fix": true/false,
        "reason": "breve spiegazione in italiano"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="qwen2.5-coder:7b", # Specifichiamo il modello che hai scaricato
            messages=[
                {"role": "system", "content": "Sei un assistente che risponde solo in JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # Bassa temperatura per risposte più logiche
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Errore Locale: {e}"

# --- TEST ---
if __name__ == "__main__":
    print(analyze_commit("fix null pointer exception", "if (x != null) { ... }"))
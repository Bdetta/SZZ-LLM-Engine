from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import miner
import analyzer
import os

app = FastAPI()

# Definiamo cosa ci aspettiamo di ricevere dall'IDE
class RepoRequest(BaseModel):
    url: str
    limit: int = 10

@app.post("/analyze")
def analyze_repository(request: RepoRequest):
    print(f"📡 Richiesta ricevuta per: {request.url}")
    
    try:
        # 1. Mining
        commits = miner.analyze_repo(request.url)
        # Limitiamo i risultati in base alla richiesta
        commits = commits[:request.limit]
        
        results = []
        
        # 2. Analisi con LLM (Ollama/OpenAI)
        for commit in commits:
            verdict = analyzer.analyze_commit(commit['message'], commit['diff'])
            results.append({
                "hash": commit['commit_hash'],
                "message": commit['message'],
                "analysis": verdict
            })
            
        return {"status": "success", "data": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Server SZZ Engine avviato su http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
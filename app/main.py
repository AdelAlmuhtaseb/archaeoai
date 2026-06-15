from fastapi import FastAPI

app = FastAPI(
    title="ArchaeoAI",
    description="AI-powered archaeological field intelligence system",
    version="0.1.0"
)

@app.get("/health")
def health():
    return {"status": "ok", "project": "ArchaeoAI"}

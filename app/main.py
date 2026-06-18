from fastapi import FastAPI
from app.models.database import create_tables
from app.api.artifacts import router as artifacts_router
from app.api.sites import router as sites_router

app = FastAPI(
    title="ArchaeoAI",
    description="AI-powered archaeological field intelligence system",
    version="0.1.0"
)

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(sites_router)
app.include_router(artifacts_router)

@app.get("/health")
def health():
    return {"status": "ok", "project": "ArchaeoAI"}
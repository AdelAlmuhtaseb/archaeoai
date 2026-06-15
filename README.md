# ArchaeoAI

AI-powered archaeological field intelligence system.

Built for real field use — logs artifact discoveries with GPS coordinates and 
photos, runs AI classification, and surfaces live insights to site supervisors.

Developed from experience on the UNESCO Dig in History project (Erasmus+ 2026).

## Stack
- FastAPI + Python
- PostgreSQL + PostGIS (geospatial queries)
- pgvector (artifact similarity search)
- Redis + Celery (async task queue)
- WebSockets (real-time field updates)
- Docker + Docker Compose
- AWS S3 (photo storage)
- Claude API (vision + classification)

## Getting started

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your values
3. Run `docker compose up --build`
4. Visit `http://localhost:8000/health`

## Project status
🚧 In active development

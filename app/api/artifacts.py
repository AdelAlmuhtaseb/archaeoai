from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.models.database import get_db
from app.models.artifact import Artifact
import uuid

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

class ArtifactCreate(BaseModel):
    site_id: str
    name: str
    description: Optional[str] = None
    period: Optional[str] = None
    condition: Optional[str] = None
    discovered_by: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@router.post("/")
def create_artifact(artifact: ArtifactCreate, db: Session = Depends(get_db)):
    location = None
    if artifact.latitude and artifact.longitude:
        location = f"POINT({artifact.longitude} {artifact.latitude})"

    db_artifact = Artifact(
        id=uuid.uuid4(),
        site_id=uuid.UUID(artifact.site_id),
        name=artifact.name,
        description=artifact.description,
        period=artifact.period,
        condition=artifact.condition,
        discovered_by=artifact.discovered_by,
        location=location
    )
    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)
    return {"id": str(db_artifact.id), "name": db_artifact.name, "status": "created"}

@router.get("/")
def list_artifacts(db: Session = Depends(get_db)):
    artifacts = db.query(Artifact).all()
    return [{"id": str(a.id), "name": a.name, "period": a.period} for a in artifacts]

@router.get("/{artifact_id}")
def get_artifact(artifact_id: str, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return {"id": str(artifact.id), "name": artifact.name, "period": artifact.period, "description": artifact.description}
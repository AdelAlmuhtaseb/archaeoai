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
def list_artifacts(
    period: Optional[str] = None,
    site_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Artifact)

    if period:
        query = query.filter(Artifact.period == period)
    if site_id:
        query = query.filter(Artifact.site_id == site_id)

    artifacts = query.all()
    return [{"id": str(a.id), "name": a.name, "period": a.period} for a in artifacts]

@router.get("/{artifact_id}")
def get_artifact(artifact_id: str, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return {"id": str(artifact.id), "name": artifact.name, "period": artifact.period, "description": artifact.description}

class ArtifactUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    period: Optional[str] = None
    condition: Optional[str] = None
    discovered_by: Optional[str] = None

@router.put("/{artifact_id}")
def update_artifact(artifact_id: str, artifact: ArtifactUpdate, db: Session = Depends(get_db)):
    db_artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not db_artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    update_data = artifact.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_artifact, field, value)

    db.commit()
    db.refresh(db_artifact)
    return {"id": str(db_artifact.id), "name": db_artifact.name, "status": "updated"}

@router.delete("/{artifact_id}")
def delete_artifact(artifact_id: str, db: Session = Depends(get_db)):
    db_artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not db_artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    db.delete(db_artifact)
    db.commit()
    return {"status": "deleted", "id": artifact_id}
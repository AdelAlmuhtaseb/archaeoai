from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.models.database import get_db
from app.models.artifact import Site
import uuid

router = APIRouter(prefix="/sites", tags=["sites"])

class SiteCreate(BaseModel):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@router.post("/")
def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    location = None
    if site.latitude and site.longitude:
        location = f"POINT({site.longitude} {site.latitude})"

    db_site = Site(
        id=uuid.uuid4(),
        name=site.name,
        location=location
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return {"id": str(db_site.id), "name": db_site.name}

@router.get("/")
def list_sites(db: Session = Depends(get_db)):
    sites = db.query(Site).all()
    return [{"id": str(s.id), "name": s.name} for s in sites]
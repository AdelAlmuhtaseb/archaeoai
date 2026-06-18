from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from geoalchemy2 import Geography
from pgvector.sqlalchemy import Vector
from datetime import datetime
import uuid

Base = declarative_base()

class Site(Base):
    __tablename__ = "sites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    location = Column(Geography(geometry_type="POINT", srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)


class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    name = Column(String(255))
    description = Column(Text)
    period = Column(String(100))
    condition = Column(String(50))
    location = Column(Geography(geometry_type="POINT", srid=4326))
    photo_url = Column(String(500))
    ai_classification = Column(Text)
    embedding = Column(Vector(1536))
    discovered_by = Column(String(255))
    discovered_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
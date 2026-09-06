from sqlalchemy import Column, String, Numeric, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
class Detection(Base):
    __tablename__ = "detections"
    id = Column(
        "detection_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    person_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )
    camera_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )
    classification = Column(
        String(30),
        nullable=False
    )
    confidence = Column(
        Numeric(5, 2),
        nullable=True
    )
    detected_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
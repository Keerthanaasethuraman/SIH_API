from sqlalchemy import Column, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
class Camera(Base):
    __tablename__ = "cameras"
    id = Column(
        "camera_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name = Column(
        "camera_name",
        String(100),
        nullable=False
    )
    camera_code = Column(
        "camera_code",
        String(50),
        nullable=False
    )
    location = Column(
        "location",
        String(255),
        nullable=False
    )
    ip_address = Column(
        "ip_address",
        String,
        nullable=True
    )
    is_active = Column(
        "is_active",
        Boolean,
        default=True
    )
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from database import Base
class Person(Base):
    __tablename__ = "persons"
    id = Column(
        "person_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    full_name = Column(
        String(150),
        nullable=False
    )
    person_code = Column(
        String(50),
        nullable=False
    )
    person_type = Column(
        String(30),
        nullable=False,
        server_default=text("'AUTHORIZED'")
    )
    status = Column(
        String(20),
        nullable=False,
        server_default=text("'ACTIVE'")
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models.detection import Detection
from auth_dependency import get_current_user
router = APIRouter(
    prefix="/api/detections",
    tags=["Detections"]
)
@router.post("/")
def create_detection(
    camera_id: UUID,
    classification: str,
    confidence: float = None,
    person_id: UUID = None,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_detection = Detection(
        camera_id=camera_id,
        classification=classification,
        confidence=confidence,
        person_id=person_id
    )
    db.add(new_detection)
    db.commit()
    db.refresh(new_detection)
    return {
        "status": "success",
        "message": "Detection created successfully",
        "detection_id": str(new_detection.id)
    }
@router.get("/")
def get_detections(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    detections = db.query(Detection).order_by(
        Detection.detected_at.desc()
    ).all()
    return detections
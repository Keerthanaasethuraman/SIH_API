from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth_dependency import get_current_user
from database import get_db
from models.camera import Camera
from models.person import Person
from models.detection import Detection
from models.alert import Alert
from models.evidence import Evidence
router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)
@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    total_cameras = db.query(Camera).count()
    active_cameras = db.query(Camera).filter(
        Camera.is_active == True
    ).count()
    total_persons = db.query(Person).count()
    total_detections = db.query(Detection).count()
    authorized_detections = db.query(Detection).filter(
        Detection.classification == "AUTHORIZED"
    ).count()
    unauthorized_detections = db.query(Detection).filter(
        Detection.classification == "UNAUTHORIZED"
    ).count()
    active_alerts = db.query(Alert).filter(
        Alert.is_resolved == False
    ).count()
    total_evidence = db.query(Evidence).count()
    return {
        "total_cameras": total_cameras,
        "active_cameras": active_cameras,
        "total_persons": total_persons,
        "total_detections": total_detections,
        "authorized_detections": authorized_detections,
        "unauthorized_detections": unauthorized_detections,
        "active_alerts": active_alerts,
        "total_evidence": total_evidence
    }
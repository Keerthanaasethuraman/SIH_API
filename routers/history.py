from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.detection import Detection
from models.alert import Alert
from auth_dependency import get_current_user
router = APIRouter(
    prefix="/api/history",
    tags=["History"]
)
@router.get("/detections")
def get_detection_history(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    detections = db.query(Detection).order_by(
        Detection.detected_at.desc()
    ).all()
    return detections
@router.get("/alerts")
def get_alert_history(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    alerts = db.query(Alert).order_by(
        Alert.created_at.desc()
    ).all()
    return alerts
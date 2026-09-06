from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.alert import Alert
from auth_dependency import get_current_user
router = APIRouter(prefix="/api/alerts", tags=["Alerts"])
@router.post("/")
def create_alert(
    camera_id: int,
    alert_type: str,
    message: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_alert = Alert(
        camera_id=camera_id,
        alert_type=alert_type,
        message=message
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return {
        "status": "success",
        "message": "Alert created successfully",
        "alert_id": new_alert.id
    }
@router.get("/")
def get_alerts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    alerts = db.query(Alert).order_by(
        Alert.created_at.desc()
    ).all()
    return alerts
@router.put("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()
    if not alert:
        return {
            "status": "error",
            "message": "Alert not found"
        }
    alert.is_resolved = True
    db.commit()
    db.refresh(alert)
    return {
        "status": "success",
        "message": "Alert resolved successfully",
        "alert_id": alert.id
    }
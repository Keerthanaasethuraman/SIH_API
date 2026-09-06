from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.evidence import Evidence
from auth_dependency import get_current_user
router = APIRouter(
    prefix="/api/evidence",
    tags=["Evidence"]
)
@router.post("/")
def create_evidence(
    detection_id: int,
    file_name: str,
    file_path: str,
    file_type: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_evidence = Evidence(
        detection_id=detection_id,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type
    )
    db.add(new_evidence)
    db.commit()
    db.refresh(new_evidence)
    return {
        "status": "success",
        "message": "Evidence created successfully",
        "evidence_id": new_evidence.id
    }
@router.get("/")
def get_evidence(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    evidence = db.query(Evidence).order_by(
        Evidence.created_at.desc()
    ).all()
    return evidence
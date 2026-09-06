from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models.camera import Camera
from auth_dependency import get_current_user
router = APIRouter(
    prefix="/api/cameras",
    tags=["Cameras"]
)
# CREATE CAMERA
@router.post("/")
def create_camera(
    name: str,
    camera_code: str,
    location: str,
    ip_address: str = None,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    new_camera = Camera(
        name=name,
        camera_code=camera_code,
        location=location,
        ip_address=ip_address
    )
    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)
    return {
        "status": "success",
        "message": "Camera added successfully",
        "camera_id": new_camera.id
    }
# GET ALL CAMERAS
@router.get("/")
def get_cameras(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    cameras = db.query(Camera).all()
    return cameras
# UPDATE CAMERA
@router.put("/{camera_id}")
def update_camera(
    camera_id: UUID,
    name: str,
    camera_code: str,
    location: str,
    ip_address: str = None,
    is_active: bool = True,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()
    if not camera:
        return {
            "status": "error",
            "message": "Camera not found"
        }
    camera.name = name
    camera.camera_code = camera_code
    camera.location = location
    camera.ip_address = ip_address
    camera.is_active = is_active
    db.commit()
    db.refresh(camera)
    return {
        "status": "success",
        "message": "Camera updated successfully",
        "camera_id": str(camera.id)
    }
# DELETE CAMERA
@router.delete("/{camera_id}")
def delete_camera(
    camera_id: UUID,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()
    if not camera:
        return {
            "status": "error",
            "message": "Camera not found"
        }
    db.delete(camera)
    db.commit()
    return {
        "status": "success",
        "message": "Camera deleted successfully",
        "camera_id": str(camera_id)
    }
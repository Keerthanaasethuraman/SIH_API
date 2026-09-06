from fastapi import FastAPI
from database import engine, Base
from models.user import User
from models.camera import Camera
from models.alert import Alert
from models.detection import Detection
from models.person import Person
from models.evidence import Evidence
from routers.auth import router as auth_router
from routers.cameras import router as camera_router
from routers.alerts import router as alert_router
from routers.detections import router as detection_router
from routers.persons import router as person_router
from routers.evidence import router as evidence_router
from routers.dashboard import router as dashboard_router
from routers.history import router as history_router
app = FastAPI()
app.include_router(auth_router)
app.include_router(camera_router)
app.include_router(alert_router)
app.include_router(detection_router)
app.include_router(person_router)
app.include_router(evidence_router)
app.include_router(dashboard_router)
app.include_router(history_router)
Base.metadata.create_all(bind=engine)
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "SIH API is running"
    }
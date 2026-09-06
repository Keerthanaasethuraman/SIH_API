from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate
from auth_utils import create_access_token
import hashlib
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()
@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if existing_user:
        return {
            "status": "error",
            "message": "Email already registered"
        }
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "status": "success",
        "message": "User registered successfully",
        "user_id": new_user.id
    }
@router.post("/login")
def login_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if not existing_user:
        return {
            "status": "error",
            "message": "Invalid email or password"
        }
    if existing_user.password != hash_password(user.password):
        return {
            "status": "error",
            "message": "Invalid email or password"
        }
    access_token = create_access_token(existing_user.id)
    return {
        "status": "success",
        "message": "Login successful",
        "user_id": existing_user.id,
        "username": existing_user.username,
        "access_token": access_token
    }
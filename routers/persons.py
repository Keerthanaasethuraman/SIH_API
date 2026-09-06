from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.person import Person
from auth_dependency import get_current_user
router = APIRouter(
    prefix="/api/persons",
    tags=["Persons"]
)
@router.post("/")
def create_person(
    full_name: str,
    person_code: str,
    person_type: str = "AUTHORIZED",
    db: Session = Depends(get_db)
):
    new_person = Person(
        full_name=full_name,
        person_code=person_code,
        person_type=person_type
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return {
        "status": "success",
        "message": "Person created successfully",
        "person_id": str(new_person.id)
    }
@router.get("/")
def get_persons(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    persons = db.query(Person).all()
    return persons
from uuid import UUID
@router.put("/{person_id}")
def update_person(
    person_id: UUID,
    full_name: str,
    person_code: str,
    person_type: str = "AUTHORIZED",
    status: str = "ACTIVE",
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(
        Person.id == person_id
    ).first()
    if not person:
        return {
            "status": "error",
            "message": "Person not found"
        }
    person.full_name = full_name
    person.person_code = person_code
    person.person_type = person_type
    person.status = status
    db.commit()
    db.refresh(person)
    return {
        "status": "success",
        "message": "Person updated successfully",
        "person_id": str(person.id)
    }
@router.delete("/{person_id}")
def delete_person(
    person_id: UUID,
    db: Session = Depends(get_db)
):
    person = db.query(Person).filter(
        Person.id == person_id
    ).first()
    if not person:
        return {
            "status": "error",
            "message": "Person not found"
        }
    db.delete(person)
    db.commit()
    return {
        "status": "success",
        "message": "Person deleted successfully",
        "person_id": str(person_id)
    }
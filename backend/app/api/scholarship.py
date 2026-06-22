from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.scholarship import ScholarshipCreate
from app.models.scholarship import Scholarship

router = APIRouter(
    prefix="/scholarship",
    tags=["Scholarship"]
)


@router.post("/create")
def create_scholarship(
    scholarship: ScholarshipCreate,
    db: Session = Depends(get_db)
):
    new_scholarship = Scholarship(
        title=scholarship.title,
        provider=scholarship.provider,
        amount=scholarship.amount,
        deadline=scholarship.deadline,
        eligibility=scholarship.eligibility,
        description=scholarship.description
    )

    db.add(new_scholarship)
    db.commit()
    db.refresh(new_scholarship)

    return {
        "message": "Scholarship Created",
        "scholarship_id": new_scholarship.id
    }


@router.get("/all")
def get_scholarships(
    db: Session = Depends(get_db)
):
    return db.query(Scholarship).all()
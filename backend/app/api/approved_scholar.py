from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.approved_scholar import ApprovedScholar
from app.schemas.approved_scholar import ApprovedScholarCreate

router = APIRouter(
    prefix="/approved-scholars",
    tags=["Approved Scholars"]
)


@router.post("/add")
def add_scholar(
    scholar: ApprovedScholarCreate,
    db: Session = Depends(get_db)
):

    new_scholar = ApprovedScholar(
        email=scholar.email,
        full_name=scholar.full_name,
        course=scholar.course,
        academic_year=scholar.academic_year
    )

    db.add(new_scholar)

    db.commit()

    db.refresh(new_scholar)

    return {
        "message": "Scholar Added"
    }


@router.get("/all")
def all_scholars(
    db: Session = Depends(get_db)
):
    return db.query(
        ApprovedScholar
    ).all()
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.scholar import (
    ScholarCreate,
    ScholarResponse,
    ScholarUpdate
)

from app.models.scholar import Scholar
from app.models.user import User

from app.core.security import verify_token


router = APIRouter(
    prefix="/scholar",
    tags=["Scholar"]
)


@router.post("/profile")
def create_profile(
    scholar: ScholarCreate,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    existing_profile = db.query(
        Scholar
    ).filter(
        Scholar.user_id == user.id
    ).first()

    if existing_profile:
        return {
            "message": "Scholar Profile Already Exists"
        }

    new_scholar = Scholar(
        user_id=user.id,

        full_name=scholar.full_name,
        phone=scholar.phone,
        country=scholar.country,
        university=scholar.university,
        course=scholar.course,
        academic_year=scholar.academic_year,
        cgpa=scholar.cgpa,
        bio=scholar.bio,

        github_url=scholar.github_url,
        portfolio_url=scholar.portfolio_url,
        linkedin_url=scholar.linkedin_url,
        project_links=scholar.project_links
    )

    db.add(new_scholar)
    db.commit()
    db.refresh(new_scholar)

    return {
        "message": "Scholar Profile Created",
        "scholar_id": new_scholar.id,
        "user_id": user.id
    }

@router.get("/my-profile")
def my_profile(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    scholar = db.query(Scholar).filter(
        Scholar.user_id == user.id
    ).first()

    return scholar

@router.get("/all")
def get_profiles(
    db: Session = Depends(get_db)
):
    return db.query(
        Scholar
    ).all()

@router.get("/{user_id}")
def get_scholar(
    user_id: int,
    db: Session = Depends(get_db)
):
    scholar = db.query(
        Scholar
    ).filter(
        Scholar.user_id == user_id
    ).first()

    if not scholar:
        raise HTTPException(
            status_code=404,
            detail="Scholar not found"
        )

    return scholar


@router.put("/profile")
def update_profile(
    scholar_data: ScholarUpdate,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    scholar = db.query(
        Scholar
    ).filter(
        Scholar.user_id == user.id
    ).first()

    if not scholar:
        raise HTTPException(
            status_code=404,
            detail="Scholar profile not found"
        )

    scholar.full_name = scholar_data.full_name
    scholar.phone = scholar_data.phone
    scholar.country = scholar_data.country
    scholar.university = scholar_data.university
    scholar.course = scholar_data.course
    scholar.academic_year = scholar_data.academic_year
    scholar.cgpa = scholar_data.cgpa
    scholar.bio = scholar_data.bio

    scholar.github_url = scholar_data.github_url
    scholar.portfolio_url = scholar_data.portfolio_url
    scholar.linkedin_url = scholar_data.linkedin_url
    scholar.project_links = scholar_data.project_links

    db.commit()
    db.refresh(scholar)

    return {
        "message": "Profile updated successfully",
        "profile": scholar
    }

@router.delete("/profile")
def delete_profile(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    scholar = db.query(
        Scholar
    ).filter(
        Scholar.user_id == user.id
    ).first()

    if not scholar:
        raise HTTPException(
            status_code=404,
            detail="Scholar profile not found"
        )

    db.delete(scholar)

    db.commit()

    return {
        "message": "Scholar profile deleted successfully"
    }
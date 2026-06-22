from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import verify_token

from app.models.user import User
from app.models.application import Application
from app.models.scholarship import Scholarship
from app.core.roles import require_role

router = APIRouter(
    prefix="/application",
    tags=["Applications"]
)


@router.post("/apply/{scholarship_id}")
def apply_scholarship(
    scholarship_id: int,
    email: str = Depends(verify_token),
    scholar=Depends(require_role("scholar")),
    db: Session = Depends(get_db)
):
    # Get logged in user
    user = db.query(User).filter(
        User.email == email
    ).first()

    # Check scholarship exists
    scholarship = db.query(Scholarship).filter(
        Scholarship.id == scholarship_id
    ).first()

    if not scholarship:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    # Prevent duplicate applications
    existing_application = db.query(Application).filter(
        Application.user_id == user.id,
        Application.scholarship_id == scholarship_id
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Already applied for this scholarship"
        )

    # Create application
    application = Application(
        user_id=user.id,
        scholarship_id=scholarship_id
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Application Submitted",
        "application_id": application.id
    }


@router.get("/my-applications")
def my_applications(
    email: str = Depends(verify_token),
    scholar=Depends(require_role("scholar")),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    applications = db.query(Application).filter(
        Application.user_id == user.id
    ).all()

    return applications

@router.get("/all")
def get_all_applications(
    db: Session = Depends(get_db)
):
    return db.query(Application).all()

@router.post("/approve/{application_id}")
def approve_application(
    application_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if application.status == "Approved":
        return {
         "message": "Already approved"
        }
    application.status = "Approved"
   

    db.commit()

    return {
        "message": "Application Approved"
    }


@router.post("/reject/{application_id}")
def reject_application(
    application_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
           status_code=404,
           detail="Application not found"
        )
    
    if application.status == "Rejected":
        return {
            "message": "Already rejected"
        }
    application.status = "Rejected"

    db.commit()

    return {
        "message": "Application Rejected"
    }

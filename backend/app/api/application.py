from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import verify_token
from app.core.roles import require_role

from app.models.user import User
from app.models.application import Application
from app.models.scholarship import Scholarship

from app.schemas.application import StatusUpdate

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
    user = db.query(User).filter(
        User.email == email
    ).first()

    scholarship = db.query(Scholarship).filter(
        Scholarship.id == scholarship_id
    ).first()

    if not scholarship:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    existing_application = db.query(Application).filter(
        Application.user_id == user.id,
        Application.scholarship_id == scholarship_id
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Already applied for this scholarship"
        )

    application = Application(
        user_id=user.id,
        scholarship_id=scholarship_id,
        status="Applied"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Application submitted successfully",
        "application_id": application.id,
        "status": application.status
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


@router.get("/{application_id}")
def get_application(
    application_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application

@router.put("/update-status/{application_id}")
def update_status(
    application_id: int,
    data: StatusUpdate,
    email: str = Depends(verify_token),
    scholar=Depends(require_role("scholar")),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    # Update status and notes
    application.status = data.status
    application.notes = data.notes

    db.commit()
    db.refresh(application)

    return {
        "message": "Status updated successfully",
        "application_id": application.id,
        "status": application.status,
        "notes": application.notes
    }
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.dependencies import get_db

from app.models.scholar import Scholar
from app.models.application import Application

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/students")
def get_students(
    db: Session = Depends(get_db)
):
    return db.query(Scholar).all()


@router.get("/applied/{scholarship_id}")
def applied_students(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    applications = db.query(Application).filter(
        Application.scholarship_id == scholarship_id
    ).all()

    result = []

    for application in applications:

        scholar = db.query(Scholar).filter(
            Scholar.user_id == application.user_id
        ).first()

        result.append({
            "application_id": application.id,
            "scholar_name":
                scholar.full_name if scholar else "Unknown",
            "status": application.status,
            "notes": application.notes,
            "created_at": application.created_at,
            "updated_at": application.updated_at
        })

    return result


@router.get("/not-applied/{scholarship_id}")
def not_applied_students(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    applied_user_ids = db.query(
        Application.user_id
    ).filter(
        Application.scholarship_id == scholarship_id
    ).all()

    applied_user_ids = [
        item[0] for item in applied_user_ids
    ]

    students = db.query(Scholar).filter(
        ~Scholar.user_id.in_(applied_user_ids)
    ).all()

    return students


@router.get("/progress/{scholarship_id}")
def scholarship_progress(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    applications = db.query(Application).filter(
        Application.scholarship_id == scholarship_id
    ).all()

    result = []

    for application in applications:

        scholar = db.query(Scholar).filter(
            Scholar.user_id == application.user_id
        ).first()

        result.append({
            "scholar_name":
                scholar.full_name if scholar else "Unknown",

            "status":
                application.status,

            "notes":
                application.notes,

            "updated_at":
                application.updated_at
        })

    return result


@router.get("/filter")
def filter_students(
    course: str = Query(None),
    academic_year: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Scholar)

    if course:
        query = query.filter(
            func.lower(Scholar.course) ==
            course.lower()
        )

    if academic_year:
        query = query.filter(
            func.lower(Scholar.academic_year) ==
            academic_year.lower()
        )

    return query.all()


@router.get("/summary/{scholarship_id}")
def scholarship_summary(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    total_students = db.query(
        Scholar
    ).count()

    applied_students = db.query(
        Application
    ).filter(
        Application.scholarship_id == scholarship_id
    ).count()

    not_applied_students = (
        total_students - applied_students
    )

    return {
        "scholarship_id": scholarship_id,
        "total_students": total_students,
        "applied_students": applied_students,
        "not_applied_students": not_applied_students
    }
from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import verify_token

from app.models.user import User
from app.models.report import Report

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.post("/achievement/{achievement_id}")
def report_achievement(
    achievement_id: int,
    reason: str,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    report = Report(
        reporter_id=user.id,
        content_type="achievement",
        content_id=achievement_id,
        reason=reason
    )

    db.add(report)

    db.commit()

    return {
        "message": "Achievement reported"
    }

@router.post("/project/{project_id}")
def report_project(
    project_id: int,
    reason: str,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    report = Report(
        reporter_id=user.id,
        content_type="project",
        content_id=project_id,
        reason=reason
    )

    db.add(report)

    db.commit()

    return {
        "message": "Project reported"
    }


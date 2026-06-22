from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import verify_token

from app.models.user import User
from app.models.scholar import Scholar
from app.models.organization import Organization
from app.models.opportunity import Opportunity
from app.models.project import Project
from app.models.achievement import Achievement
from app.models.organization_invite import OrganizationInvite
from app.models.report import Report
from app.models.connection import Connection
from app.models.message import Message
from app.core.roles import require_role

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/pending-scholars")
def pending_scholars(
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    return db.query(
        Scholar
    ).filter(
        Scholar.is_verified == False
    ).all()


@router.post("/verify-scholar/{scholar_id}")
def verify_scholar(
    scholar_id: int,
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    scholar = db.query(
        Scholar
    ).filter(
        Scholar.id == scholar_id
    ).first()

    if not scholar:
        raise HTTPException(
            status_code=404,
            detail="Scholar not found"
        )

    scholar.is_verified = True

    db.commit()

    return {
        "message": "Scholar Verified"
    }


@router.get("/pending-organizations")
def pending_organizations(
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    return db.query(
        Organization
    ).filter(
        Organization.is_verified == False
    ).all()


@router.post("/verify-organization/{organization_id}")
def verify_organization(
    organization_id: int,
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    organization = db.query(
        Organization
    ).filter(
        Organization.id == organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    organization.is_verified = True

    db.commit()

    return {
        "message": "Organization Verified"
    }


@router.get("/stats")
def platform_stats(
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    total_users = db.query(
        User
    ).count()

    total_scholars = db.query(
        Scholar
    ).count()

    total_organizations = db.query(
        Organization
    ).count()

    total_opportunities = db.query(
        Opportunity
    ).count()

    total_projects = db.query(
        Project
    ).count()

    total_achievements = db.query(
        Achievement
    ).count()

    total_connections = db.query(
        Connection
    ).count()

    total_messages = db.query(
        Message
    ).count()

    pending_reports = db.query(
        Report
    ).filter(
        Report.status != "Resolved"
    ).count()

    return {
        "total_users": total_users,
        "total_scholars": total_scholars,
        "total_organizations": total_organizations,
        "total_opportunities": total_opportunities,
        "total_projects": total_projects,
        "total_achievements": total_achievements,
        "total_connections": total_connections,
        "total_messages": total_messages,
        "pending_reports": pending_reports
    }

@router.post("/invite-organization")
def invite_organization(
    email: str,
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    existing = db.query(
        OrganizationInvite
    ).filter(
        OrganizationInvite.email == email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Invitation already exists"
        )

    invite = OrganizationInvite(
        email=email
    )

    db.add(invite)

    db.commit()

    db.refresh(invite)

    return {
        "message": "Invitation sent",
        "invite_id": invite.id
    }

@router.get("/invitations")
def all_invitations(
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    return db.query(
        OrganizationInvite
    ).all()

@router.get("/reports")
def all_reports(
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    return db.query(
        Report
    ).all()

@router.post("/resolve-report/{report_id}")
def resolve_report(
    report_id: int,
    admin=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    report = db.query(
        Report
    ).filter(
        Report.id == report_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    report.status = "Resolved"

    db.commit()

    return {
        "message": "Report resolved"
    }


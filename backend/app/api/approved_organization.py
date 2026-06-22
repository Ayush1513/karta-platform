from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.approved_organization import (
    ApprovedOrganization
)

from app.schemas.approved_organization import (
    ApprovedOrganizationCreate
)

router = APIRouter(
    prefix="/approved-organizations",
    tags=["Approved Organizations"]
)


@router.post("/add")
def add_organization(
    organization: ApprovedOrganizationCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(
        ApprovedOrganization
    ).filter(
        ApprovedOrganization.email
        == organization.email
    ).first()

    if existing:
        return {
            "message":
            "Organization already exists"
        }

    new_organization = (
        ApprovedOrganization(
            email=organization.email,
            organization_name=
            organization.organization_name
        )
    )

    db.add(new_organization)

    db.commit()

    db.refresh(new_organization)

    return {
        "message":
        "Organization added successfully"
    }


@router.get("/all")
def get_organizations(
    db: Session = Depends(get_db)
):

    return db.query(
        ApprovedOrganization
    ).all()
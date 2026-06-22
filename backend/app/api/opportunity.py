from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.dependencies import get_db


from app.models.organization import Organization
from app.models.opportunity import Opportunity

from app.schemas.opportunity import OpportunityCreate
from app.core.roles import require_role

router = APIRouter(
    prefix="/opportunity",
    tags=["Opportunity"]
)


@router.post("/create")
def create_opportunity(
    data: OpportunityCreate,
    organization_user=Depends(
        require_role("organization")
    ),
    db: Session = Depends(get_db)
):

    organization = db.query(
        Organization
    ).filter(
        Organization.user_id == organization_user.id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization profile not found"
        )

    opportunity = Opportunity(
        organization_id=organization.id,
        title=data.title,
        type=data.type,
        skills_required=data.skills_required,
        description=data.description,
        location=data.location
    )

    db.add(opportunity)

    db.commit()

    db.refresh(opportunity)

    return {
        "message": "Opportunity Created",
        "opportunity_id": opportunity.id
    }


@router.get("/all")
def all_opportunities(
    db: Session = Depends(get_db)
):

    return db.query(
        Opportunity
    ).all()

@router.get("/search")
def search_opportunities(
    skill: str = Query(None),
    location: str = Query(None),
    type: str = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Opportunity)

    if location:
        query = query.filter(
            func.lower(
                Opportunity.location
            ).contains(
                location.lower()
            )
        )

    if type:
        query = query.filter(
            func.lower(
                Opportunity.type
            ) == type.lower()
        )

    opportunities = query.all()

    if skill:

        filtered = []

        for opportunity in opportunities:

            skills = []

            if opportunity.skills_required:
                skills = [
                    s.strip().lower()
                    for s in opportunity.skills_required.split(",")
                ]

            if skill.lower() in skills:
                filtered.append(opportunity)

        return filtered

    return opportunities


@router.get("/{opportunity_id}")
def get_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db)
):

    opportunity = db.query(
        Opportunity
    ).filter(
        Opportunity.id == opportunity_id
    ).first()

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    return opportunity


@router.put("/{opportunity_id}")
def update_opportunity(
    opportunity_id: int,
    data: OpportunityCreate,
    organization_user=Depends(
        require_role("organization")
    ),
    db: Session = Depends(get_db)
):
    organization = db.query(
        Organization
    ).filter(
        Organization.user_id == organization_user.id
    ).first()

    opportunity = db.query(
        Opportunity
    ).filter(
        Opportunity.id == opportunity_id,
        Opportunity.organization_id == organization.id
    ).first()

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    opportunity.title = data.title
    opportunity.type = data.type
    opportunity.skills_required = data.skills_required
    opportunity.description = data.description
    opportunity.location = data.location

    db.commit()

    return {
        "message": "Opportunity Updated"
    }


@router.delete("/{opportunity_id}")
def delete_opportunity(
    opportunity_id: int,
    organization_user=Depends(
        require_role("organization")
    ),
    db: Session = Depends(get_db)
):

    organization = db.query(
        Organization
    ).filter(
        Organization.user_id == organization_user.id
    ).first()

    opportunity = db.query(
        Opportunity
    ).filter(
        Opportunity.id == opportunity_id,
        Opportunity.organization_id == organization.id
    ).first()

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    db.delete(opportunity)

    db.commit()

    return {
        "message": "Opportunity Deleted"
    }
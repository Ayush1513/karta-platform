from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.core.security import verify_token

from app.models.user import User
from app.models.organization import Organization
from app.models.opportunity import Opportunity

from app.schemas.organization import OrganizationCreate
from app.models.scholar import Scholar
from app.models.skill import Skill

router = APIRouter(
    prefix="/organization",
    tags=["Organization"]
)


@router.post("/profile")
def create_organization_profile(
    data: OrganizationCreate,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    existing = db.query(
        Organization
    ).filter(
        Organization.user_id == user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Organization profile already exists"
        )

    organization = Organization(
        user_id=user.id,
        organization_name=data.organization_name,
        industry=data.industry,
        website=data.website,
        location=data.location,
        description=data.description
    )

    db.add(organization)

    db.commit()

    db.refresh(organization)

    return organization


@router.get("/my-profile")
def my_organization_profile(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    return db.query(
        Organization
    ).filter(
        Organization.user_id == user.id
    ).first()


@router.get("/all")
def get_all_organizations(
    db: Session = Depends(get_db)
):

    return db.query(
        Organization
    ).all()

@router.get("/search")
def search_organizations(
    keyword: str,
    db: Session = Depends(get_db)
):

    return db.query(
        Organization
    ).filter(
        Organization.organization_name.contains(keyword)
    ).all()

@router.get("/search-scholars")
def search_scholars(
    course: str = None,
    skill: str = None,
    academic_year: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Scholar)

    if course:
        query = query.filter(
            Scholar.course.contains(course)
        )

    if academic_year:
        query = query.filter(
            Scholar.academic_year.contains(
                academic_year
            )
        )

    scholars = query.all()

    if skill:

        filtered_scholars = []

        for scholar in scholars:

            skill_exists = db.query(
                Skill
            ).filter(
                Skill.user_id == scholar.user_id,
                Skill.skill_name.contains(skill)
            ).first()

            if skill_exists:
                filtered_scholars.append(
                    scholar
                )

        return filtered_scholars

    return scholars

@router.get("/match/{opportunity_id}")
def match_scholars_for_opportunity(
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

    required_skills = []

    if opportunity.skills_required:

        required_skills = [
            skill.strip().lower()
            for skill in
            opportunity.skills_required.split(",")
        ]

    scholars = db.query(
        Scholar
    ).all()

    results = []

    for scholar in scholars:

        scholar_skills = db.query(
            Skill
        ).filter(
            Skill.user_id == scholar.user_id
        ).all()

        scholar_skill_names = [
            skill.skill_name.lower()
            for skill in scholar_skills
        ]

        matched = len(
            set(required_skills)
            &
            set(scholar_skill_names)
        )

        total_required = max(
            len(required_skills),
            1
        )

        score = int(
            (matched / total_required) * 100
        )

        results.append(
            {
                "scholar_id": scholar.id,
                "full_name": scholar.full_name,
                "course": scholar.course,
                "match_score": score
            }
        )

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results


@router.get("/{organization_id}")
def get_single_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Organization
    ).filter(
        Organization.id == organization_id
    ).first()

@router.put("/profile")
def update_organization_profile(
    data: OrganizationCreate,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    organization = db.query(
        Organization
    ).filter(
        Organization.user_id == user.id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    organization.organization_name = data.organization_name
    organization.industry = data.industry
    organization.website = data.website
    organization.location = data.location
    organization.description = data.description

    db.commit()

    return {
        "message": "Organization Updated"
    }

@router.delete("/profile")
def delete_organization_profile(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    organization = db.query(
        Organization
    ).filter(
        Organization.user_id == user.id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    db.delete(organization)

    db.commit()

    return {
        "message": "Organization Deleted"
    }
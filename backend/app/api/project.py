from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.core.security import verify_token

from app.models.user import User
from app.models.project import Project

from app.schemas.project import ProjectCreate
from app.core.roles import require_role
router = APIRouter(
    prefix="/project",
    tags=["Project"]
)


@router.post("/create")
def create_project(
    project: ProjectCreate,
    email: str = Depends(verify_token),
    scholar=Depends(
        require_role("scholar")
    ),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    new_project = Project(
        user_id=user.id,
        title=project.title,
        description=project.description,
        tech_stack=project.tech_stack,
        github_url=project.github_url,
        live_url=project.live_url,
        is_pinned=project.is_pinned
    )

    db.add(new_project)

    db.commit()

    db.refresh(new_project)

    return {
        "message": "Project Created",
        "project_id": new_project.id
    }


@router.get("/{user_id}")
def get_projects(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Project
    ).filter(
        Project.user_id == user_id
    ).all()

@router.put("/{project_id}")
def update_project(
    project_id: int,
    project: ProjectCreate,
    email: str = Depends(verify_token),
    scholar=Depends(
        require_role("scholar")
    ),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    existing_project = db.query(
        Project
    ).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()

    if not existing_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    existing_project.title = project.title
    existing_project.description = project.description
    existing_project.tech_stack = project.tech_stack
    existing_project.github_url = project.github_url
    existing_project.live_url = project.live_url
    existing_project.is_pinned = project.is_pinned

    db.commit()

    return {
        "message": "Project Updated"
    }


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    email: str = Depends(verify_token),
    scholar=Depends(
        require_role("scholar")
    ),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    project = db.query(
        Project
    ).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)

    db.commit()

    return {
        "message": "Project Deleted"
    }

@router.get("/details/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(
        Project
    ).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project
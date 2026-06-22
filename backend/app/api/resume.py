import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.resume import Resume
from app.core.roles import require_role

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_FOLDER = "uploads/resumes"

# Create folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    scholar=Depends(
        require_role("scholar")
    ),
    db: Session = Depends(get_db)
):

    # PDF validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # File size validation (5 MB)
    contents = file.file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File exceeds 5 MB limit"
        )

    file.file.seek(0)

    filename = f"user_{user_id}.pdf"
    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    existing = db.query(Resume).filter(
        Resume.user_id == user_id
    ).first()

    if existing:
        existing.file_name = filename
        existing.file_path = filepath
    else:
        resume = Resume(
            user_id=user_id,
            file_name=filename,
            file_path=filepath
        )
        db.add(resume)

    db.commit()

    return {
        "message": "Resume uploaded successfully",
        "file_name": filename,
        "file_path": filepath
    }


@router.get("/{user_id}")
def get_resume(
    user_id: int,
    db: Session = Depends(get_db)
):

    resume = db.query(Resume).filter(
        Resume.user_id == user_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "file_name": resume.file_name,
        "file_path": resume.file_path
    }


@router.delete("/{user_id}")
def delete_resume(
    user_id: int,
    db: Session = Depends(get_db)
):

    resume = db.query(Resume).filter(
        Resume.user_id == user_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    db.delete(resume)
    db.commit()

    return {
        "message": "Resume deleted successfully"
    }
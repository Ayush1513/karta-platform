from pydantic import BaseModel
from typing import Optional

class ScholarCreate(BaseModel):
    full_name: str
    phone: str
    country: str
    university: str
    course: str
    academic_year: str
    cgpa: str
    bio: str

    github_url: str | None = None
    portfolio_url: str | None = None
    linkedin_url: str | None = None
    project_links: str | None = None


class ScholarResponse(BaseModel):
    id: int

    full_name: str
    phone: str
    country: str
    university: str
    course: str
    academic_year: str
    cgpa: str
    bio: str

    github_url: str | None = None
    portfolio_url: str | None = None
    linkedin_url: str | None = None
    project_links: str | None = None

    class Config:
        from_attributes = True

class ScholarUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    university: Optional[str] = None
    course: Optional[str] = None
    academic_year: Optional[str] = None
    cgpa: Optional[str] = None
    bio: Optional[str] = None

    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    project_links: Optional[str] = None
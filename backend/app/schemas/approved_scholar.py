from pydantic import BaseModel


class ApprovedScholarCreate(BaseModel):
    email: str
    full_name: str
    course: str
    academic_year: str
    
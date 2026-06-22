from pydantic import BaseModel


class ScholarshipCreate(BaseModel):
    title: str
    provider: str
    amount: str
    deadline: str
    eligibility: str
    description: str


class ScholarshipResponse(BaseModel):
    id: int
    title: str
    provider: str
    amount: str
    deadline: str
    eligibility: str
    description: str

    class Config:
        from_attributes = True
from pydantic import BaseModel


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    scholarship_id: int
    status: str

    class Config:
        from_attributes = True
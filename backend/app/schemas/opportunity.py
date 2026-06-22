from pydantic import BaseModel


class OpportunityCreate(BaseModel):

    title: str

    type: str

    skills_required: str

    description: str

    location: str
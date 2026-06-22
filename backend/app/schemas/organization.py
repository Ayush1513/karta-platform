from pydantic import BaseModel


class OrganizationCreate(BaseModel):

    organization_name: str

    industry: str

    website: str

    location: str

    description: str


class OrganizationUpdate(BaseModel):

    organization_name: str

    industry: str

    website: str

    location: str

    description: str
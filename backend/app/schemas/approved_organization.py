from pydantic import BaseModel


class ApprovedOrganizationCreate(
    BaseModel
):
    email: str
    organization_name: str
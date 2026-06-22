from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from app.database.database import Base


class ApprovedOrganization(Base):
    __tablename__ = "approved_organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True
    )

    organization_name = Column(
        String
    )

    is_registered = Column(
        Boolean,
        default=False
    )
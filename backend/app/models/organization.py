from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean

from app.database.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    organization_name = Column(
        String
    )

    industry = Column(
        String
    )

    website = Column(
        String
    )

    location = Column(
        String
    )

    description = Column(
        String
    )

    is_verified = Column(
    Boolean,
    default=False
    )
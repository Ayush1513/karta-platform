from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from app.database.database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    title = Column(String)

    type = Column(String)

    skills_required = Column(Text)

    description = Column(Text)

    location = Column(String)
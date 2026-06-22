from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class Scholar(Base):
    __tablename__ = "scholars"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    full_name = Column(String)

    phone = Column(String)

    country = Column(String)

    university = Column(String)

    course = Column(String)

    academic_year = Column(String)

    cgpa = Column(String)

    bio = Column(String)

    github_url = Column(
        String,
        nullable=True
    )

    portfolio_url = Column(
        String,
        nullable=True
    )

    linkedin_url = Column(
        String,
        nullable=True
    )

    project_links = Column(
        String,
        nullable=True
    )
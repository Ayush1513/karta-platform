from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from app.database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    title = Column(
        String
    )

    description = Column(
        String
    )

    tech_stack = Column(
        String
    )

    github_url = Column(
        String,
        nullable=True
    )

    live_url = Column(
        String,
        nullable=True
    )

    is_pinned = Column(
        Boolean,
        default=False
    )
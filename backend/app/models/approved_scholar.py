from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from app.database.database import Base


class ApprovedScholar(Base):
    __tablename__ = "approved_scholars"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True
    )

    full_name = Column(String)

    course = Column(String)

    academic_year = Column(String)

    is_registered = Column(
        Boolean,
        default=False
    )
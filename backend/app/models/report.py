from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    reporter_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    content_type = Column(
        String
    )

    content_id = Column(
        Integer
    )

    reason = Column(
        String
    )

    status = Column(
        String,
        default="Pending"
    )
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

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

    image_url = Column(
    String,
    nullable=True
    )

    achievement_type = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    is_pinned = Column(
    Integer,
    default=0
    )
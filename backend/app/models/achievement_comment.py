from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base


class AchievementComment(Base):
    __tablename__ = "achievement_comments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    achievement_id = Column(
        Integer,
        ForeignKey("achievements.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    comment = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
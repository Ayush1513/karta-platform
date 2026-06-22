from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from app.database.database import Base


class AchievementLike(Base):
    __tablename__ = "achievement_likes"

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
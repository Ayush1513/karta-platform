from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedback"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    recommendation_id = Column(
        Integer,
        ForeignKey("recommendations.id")
    )

    feedback = Column(
        String
    )
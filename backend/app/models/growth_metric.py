from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.database.database import Base


class GrowthMetric(Base):
    __tablename__ = "growth_metrics"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    profile_score = Column(Integer)
    skills_count = Column(Integer)
    recommendations_count = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
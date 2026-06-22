from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    opportunity_id = Column(
        Integer,
        ForeignKey("opportunities.id")
    )

    relevance_score = Column(
        Integer
    )

    reason = Column(
        String
    )

    status = Column(
        String,
        default="recommended"
    )
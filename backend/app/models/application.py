from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime
from app.database.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    scholarship_id = Column(Integer, ForeignKey("scholarships.id"))

    status = Column(String, default="Pending")
    created_at = Column(
    DateTime,
    default=datetime.utcnow
    )
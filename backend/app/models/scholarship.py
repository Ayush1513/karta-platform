from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    provider = Column(String)
    amount = Column(String)
    deadline = Column(String)
    eligibility = Column(String)
    description = Column(String)
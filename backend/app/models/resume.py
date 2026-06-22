from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    file_name = Column(String)
    file_path = Column(String)
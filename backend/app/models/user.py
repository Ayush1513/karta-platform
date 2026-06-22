from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)

    password_hash = Column(String)

    role = Column(String)

    is_verified = Column(Boolean, default=False)
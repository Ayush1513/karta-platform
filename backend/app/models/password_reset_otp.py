from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base


class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String
    )

    otp = Column(
        String
    )

    is_used = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
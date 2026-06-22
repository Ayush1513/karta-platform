from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    sender_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    receiver_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    message = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
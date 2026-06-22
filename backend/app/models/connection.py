from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class Connection(Base):
    __tablename__ = "connections"

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

    status = Column(
        String,
        default="Pending"
    )
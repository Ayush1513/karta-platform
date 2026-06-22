from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.dependencies import get_db
from app.core.security import verify_token

from app.models.user import User
from app.models.message import Message
from app.models.connection import Connection

router = APIRouter(
    prefix="/message",
    tags=["Message"]
)

@router.post("/send/{user_id}")
def send_message(
    user_id: int,
    message: str,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    sender = db.query(User).filter(
        User.email == email
    ).first()

    connection = db.query(
        Connection
    ).filter(
        (
            (Connection.sender_id == sender.id) &
            (Connection.receiver_id == user_id)
        ) |
        (
            (Connection.sender_id == user_id) &
            (Connection.receiver_id == sender.id)
        ),
        Connection.status == "Accepted"
    ).first()

    if not connection:
        raise HTTPException(
            status_code=403,
            detail="You are not connected with this user"
        )

    new_message = Message(
        sender_id=sender.id,
        receiver_id=user_id,
        message=message
    )

    db.add(new_message)

    db.commit()

    return {
        "message": "Message Sent"
    }

@router.get("/conversation/{user_id}")
def conversation(
    user_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    current_user = db.query(User).filter(
        User.email == email
    ).first()

    messages = db.query(
        Message
    ).filter(
        or_(
            (
                (Message.sender_id == current_user.id) &
                (Message.receiver_id == user_id)
            ),
            (
                (Message.sender_id == user_id) &
                (Message.receiver_id == current_user.id)
            )
        )
    ).all()

    return messages

@router.get("/inbox")
def inbox(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    current_user = db.query(User).filter(
        User.email == email
    ).first()

    messages = db.query(
        Message
    ).filter(
        Message.receiver_id == current_user.id
    ).all()

    return messages


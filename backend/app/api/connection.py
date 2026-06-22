from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import verify_token

from app.models.user import User
from app.models.connection import Connection

router = APIRouter(
    prefix="/connection",
    tags=["Connection"]
)

@router.post("/request/{user_id}")
def send_request(
    user_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    sender = db.query(User).filter(
        User.email == email
    ).first()

    if sender.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot connect with yourself"
        )

    existing = db.query(
        Connection
    ).filter(
        Connection.sender_id == sender.id,
        Connection.receiver_id == user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Request already sent"
        )

    connection = Connection(
        sender_id=sender.id,
        receiver_id=user_id
    )

    db.add(connection)

    db.commit()

    return {
        "message": "Connection Request Sent"
    }

@router.post("/accept/{connection_id}")
def accept_request(
    connection_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    connection = db.query(
        Connection
    ).filter(
        Connection.id == connection_id,
        Connection.receiver_id == user.id
    ).first()

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    connection.status = "Accepted"

    db.commit()

    return {
        "message": "Connection Accepted"
    }

@router.post("/reject/{connection_id}")
def reject_request(
    connection_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    connection = db.query(
        Connection
    ).filter(
        Connection.id == connection_id,
        Connection.receiver_id == user.id
    ).first()

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    connection.status = "Rejected"

    db.commit()

    return {
        "message": "Connection Rejected"
    }

@router.get("/my-requests")
def my_requests(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    return db.query(
        Connection
    ).filter(
        Connection.receiver_id == user.id,
        Connection.status == "Pending"
    ).all()

@router.get("/my-connections")
def my_connections(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    return db.query(
        Connection
    ).filter(
        (
            Connection.sender_id == user.id
        ) |
        (
            Connection.receiver_id == user.id
        ),
        Connection.status == "Accepted"
    ).all()

@router.delete("/{connection_id}")
def remove_connection(
    connection_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    connection = db.query(
        Connection
    ).filter(
        Connection.id == connection_id,
        Connection.status == "Accepted"
    ).first()

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Connection not found"
        )

    if (
        connection.sender_id != user.id and
        connection.receiver_id != user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    db.delete(connection)

    db.commit()

    return {
        "message": "Connection Removed"
    }
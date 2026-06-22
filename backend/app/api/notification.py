from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import verify_token

from app.models.user import User
from app.models.notification import Notification

router = APIRouter(
    prefix="/notification",
    tags=["Notification"]
)


@router.get("/my")
def my_notifications(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    notifications = db.query(
        Notification
    ).filter(
        Notification.user_id == user.id
    ).order_by(
        Notification.id.desc()
    ).all()

    return notifications


@router.post("/read/{notification_id}")
def mark_as_read(
    notification_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    notification = db.query(
        Notification
    ).filter(
        Notification.id == notification_id,
        Notification.user_id == user.id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()

    return {
        "message": "Notification marked as read"
    }


@router.get("/unread-count")
def unread_count(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    count = db.query(
        Notification
    ).filter(
        Notification.user_id == user.id,
        Notification.is_read == False
    ).count()

    return {
        "unread_notifications": count
    }
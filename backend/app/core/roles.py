from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.core.security import verify_token
from app.models.user import User


def require_role(role: str):

    def role_checker(
        email: str = Depends(verify_token),
        db: Session = Depends(get_db)
    ):

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )

        if user.role != role:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return role_checker
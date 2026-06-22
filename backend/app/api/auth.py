from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from random import randint

from fastapi.security import OAuth2PasswordRequestForm

from app.database.dependencies import get_db

from app.schemas.user import UserCreate

from app.schemas.password_reset import (
    ForgotPasswordRequest,
    VerifyOTPRequest,
    ResetPasswordRequest
)

from app.models.user import User
from app.models.approved_scholar import ApprovedScholar
from app.models.approved_organization import ApprovedOrganization
from app.models.password_reset_otp import PasswordResetOTP

from app.services.email_service import send_otp_email

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

router = APIRouter(
prefix="/auth",
tags=["Authentication"]
)

@router.get("/test")
def test_auth():
    return {
      "message": "Auth API Working"
    }

@router.get("/users")
def get_users(
db: Session = Depends(get_db)
):
    return db.query(User).all()

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        User
    ).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }

    # Scholar Registration
    if user.role == "scholar":

        approved_scholar = db.query(
            ApprovedScholar
        ).filter(
            ApprovedScholar.email == user.email
        ).first()

        if not approved_scholar:
            return {
                "message":
                "Registration denied. Scholar email is not approved by Karta."
            }

        if approved_scholar.is_registered:
            return {
                "message":
                "Scholar account already activated."
            }

        approved_scholar.is_registered = True

    # Organization Registration
    elif user.role == "organization":

        approved_organization = db.query(
            ApprovedOrganization
        ).filter(
            ApprovedOrganization.email == user.email
        ).first()

        if not approved_organization:
            return {
                "message":
                "Registration denied. Organization email is not approved by Karta."
            }

        if approved_organization.is_registered:
            return {
                "message":
                "Organization account already activated."
            }

        approved_organization.is_registered = True

    # Admin Registration Block
    elif user.role == "admin":

        return {
            "message":
            "Admin accounts cannot be self-registered."
        }

    else:

        return {
            "message":
            "Invalid role selected."
        }

    new_user = User(
        email=user.email,
        password_hash=hash_password(
            user.password
        ),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "role": new_user.role
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        return {
            "message": "Invalid email or password"
        }

    if not verify_password(
        form_data.password,
        db_user.password_hash
    ):
        return {
            "message": "Invalid email or password"
        }

    token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        return {
            "message": "Email not found"
        }

    # Delete previous OTPs
    db.query(
        PasswordResetOTP
    ).filter(
        PasswordResetOTP.email == request.email
    ).delete()

    otp = str(
        randint(100000, 999999)
    )

    otp_record = PasswordResetOTP(
        email=request.email,
        otp=otp
    )

    db.add(otp_record)
    db.commit()

    try:

        send_otp_email(
            request.email,
            otp
        )

        return {
            "message": "OTP sent to email"
        }

    except Exception as e:

        return {
            "message": "Failed to send OTP",
            "error": str(e)
        }


@router.post("/verify-otp")
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    otp_record = db.query(
        PasswordResetOTP
    ).filter(
        PasswordResetOTP.email == request.email,
        PasswordResetOTP.otp == request.otp,
        PasswordResetOTP.is_used == False
    ).first()

    if not otp_record:
        return {
            "message": "Invalid OTP"
        }

    return {
        "message": "OTP Verified"
    }


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    otp_record = db.query(
        PasswordResetOTP
    ).filter(
        PasswordResetOTP.email == request.email,
        PasswordResetOTP.otp == request.otp,
        PasswordResetOTP.is_used == False
    ).first()

    if not otp_record:
        return {
            "message": "Invalid OTP"
        }

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    user.password_hash = hash_password(
        request.new_password
    )

    otp_record.is_used = True

    db.commit()

    return {
        "message": "Password reset successful"
    }

@router.get("/me")
def get_me(
email: str = Depends(verify_token)
):
    return {
      "logged_in_user": email
    }

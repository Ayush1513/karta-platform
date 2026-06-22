from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.core.security import verify_token

from app.models.user import User
from app.models.achievement import Achievement

from app.schemas.achievement import AchievementCreate
from app.models.achievement_save import AchievementSave
from app.models.achievement_like import AchievementLike
from app.models.achievement_comment import AchievementComment
from app.core.roles import require_role

from app.schemas.comment import CommentCreate

router = APIRouter(
    prefix="/achievement",
    tags=["Achievement"]
)


@router.post("/create")
def create_achievement(
    achievement: AchievementCreate,
    email: str = Depends(verify_token),
    scholar=Depends(require_role("scholar")),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    new_achievement = Achievement(
    user_id=user.id,
    title=achievement.title,
    description=achievement.description,
    achievement_type=achievement.achievement_type,
    image_url=achievement.image_url
    )

    db.add(new_achievement)

    db.commit()

    db.refresh(new_achievement)

    return {
        "message": "Achievement Created",
        "achievement_id": new_achievement.id
    }

@router.get("/feed")
def achievement_feed(
    db: Session = Depends(get_db)
):

    return db.query(
        Achievement
    ).order_by(
        Achievement.created_at.desc()
    ).all()


@router.get("/all")
def get_all_achievements(
    db: Session = Depends(get_db)
):

    return db.query(
        Achievement
    ).all()

@router.get("/my-achievements")
def my_achievements(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    return db.query(
        Achievement
    ).filter(
        Achievement.user_id == user.id
    ).order_by(
        Achievement.created_at.desc()
    ).all()


@router.get("/details/{achievement_id}")
def achievement_details(
    achievement_id: int,
    db: Session = Depends(get_db)
):

    achievement = db.query(
        Achievement
    ).filter(
        Achievement.id == achievement_id
    ).first()

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    return achievement


@router.get("/{user_id}")
def get_user_achievements(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Achievement
    ).filter(
        Achievement.user_id == user_id
    ).all()


@router.put("/{achievement_id}")
def update_achievement(
    achievement_id: int,
    achievement: AchievementCreate,
    email: str = Depends(verify_token),
    scholar=Depends(require_role("scholar")),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    existing = db.query(
        Achievement
    ).filter(
        Achievement.id == achievement_id,
        Achievement.user_id == user.id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    existing.title = achievement.title
    existing.description = achievement.description
    existing.achievement_type = achievement.achievement_type

    db.commit()

    return {
        "message": "Achievement Updated"
    }


@router.delete("/{achievement_id}")
def delete_achievement(
    achievement_id: int,
    email: str = Depends(verify_token),
    scholar=Depends(require_role("scholar")),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    achievement = db.query(
        Achievement
    ).filter(
        Achievement.id == achievement_id,
        Achievement.user_id == user.id
    ).first()

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    db.delete(achievement)

    db.commit()

    return {
        "message": "Achievement Deleted"
    }

@router.post("/{achievement_id}/like")
def like_achievement(
    achievement_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    existing = db.query(
        AchievementLike
    ).filter(
        AchievementLike.achievement_id == achievement_id,
        AchievementLike.user_id == user.id
    ).first()

    if existing:
        return {
            "message": "Already liked"
        }

    like = AchievementLike(
        achievement_id=achievement_id,
        user_id=user.id
    )

    db.add(like)

    db.commit()

    return {
        "message": "Achievement liked"
    }

@router.get("/{achievement_id}/likes")
def get_likes_count(
    achievement_id: int,
    db: Session = Depends(get_db)
):

    count = db.query(
        AchievementLike
    ).filter(
        AchievementLike.achievement_id
        == achievement_id
    ).count()

    return {
        "achievement_id": achievement_id,
        "likes": count
    }


@router.post("/{achievement_id}/comment")
def comment_achievement(
    achievement_id: int,
    data: CommentCreate,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    comment = AchievementComment(
        achievement_id=achievement_id,
        user_id=user.id,
        comment=data.comment
    )

    db.add(comment)

    db.commit()

    return {
        "message": "Comment added"
    }

@router.get("/{achievement_id}/comments")
def get_comments(
    achievement_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        AchievementComment
    ).filter(
        AchievementComment.achievement_id
        == achievement_id
    ).all()

@router.post("/{achievement_id}/save")
def save_achievement(
    achievement_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    existing = db.query(
        AchievementSave
    ).filter(
        AchievementSave.user_id == user.id,
        AchievementSave.achievement_id == achievement_id
    ).first()

    if existing:
        return {
            "message": "Already saved"
        }

    save = AchievementSave(
        user_id=user.id,
        achievement_id=achievement_id
    )

    db.add(save)

    db.commit()

    return {
        "message": "Achievement saved"
    }

@router.get("/saved")
def get_saved_achievements(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    saved = db.query(
        Achievement
    ).join(
        AchievementSave,
        Achievement.id == AchievementSave.achievement_id
    ).filter(
        AchievementSave.user_id == user.id
    ).all()

    return saved

@router.delete("/{achievement_id}/save")
def unsave_achievement(
    achievement_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    saved = db.query(
        AchievementSave
    ).filter(
        AchievementSave.achievement_id == achievement_id,
        AchievementSave.user_id == user.id
    ).first()

    if not saved:
        raise HTTPException(
            status_code=404,
            detail="Achievement not saved"
        )

    db.delete(saved)

    db.commit()

    return {
        "message": "Achievement removed from saved"
    }

@router.post("/{achievement_id}/pin")
def pin_achievement(
    achievement_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    achievement = db.query(
        Achievement
    ).filter(
        Achievement.id == achievement_id,
        Achievement.user_id == user.id
    ).first()

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    achievement.is_pinned = 1

    db.commit()

    return {
        "message": "Achievement pinned"
    }

@router.post("/{achievement_id}/unpin")
def unpin_achievement(
    achievement_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    achievement = db.query(
        Achievement
    ).filter(
        Achievement.id == achievement_id,
        Achievement.user_id == user.id
    ).first()

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    achievement.is_pinned = 0

    db.commit()

    return {
        "message": "Achievement unpinned"
    }
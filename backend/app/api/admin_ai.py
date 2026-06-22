from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.opportunity import Opportunity
from app.models.scholar import Scholar
from app.models.skill import Skill
from app.models.project import Project
from app.models.achievement import Achievement
from app.models.resume import Resume

router = APIRouter(
    prefix="/admin",
    tags=["Admin AI"]
)


@router.get("/match/{opportunity_id}")
def match_scholars(
    opportunity_id: int,
    db: Session = Depends(get_db)
):

    opportunity = db.query(
        Opportunity
    ).filter(
        Opportunity.id == opportunity_id
    ).first()

    if not opportunity:
        return {
            "message": "Opportunity not found"
        }

    required_skills = []

    if opportunity.skills_required:
        required_skills = [
            skill.strip().lower()
            for skill in opportunity.skills_required.split(",")
        ]

    scholars = db.query(
        Scholar
    ).all()

    results = []

    for scholar in scholars:

        scholar_skills = db.query(
            Skill
        ).filter(
            Skill.user_id == scholar.user_id
        ).all()

        scholar_skill_names = [
            skill.skill_name.lower()
            for skill in scholar_skills
        ]

        # --------------------
        # Skills Score (40)
        # --------------------

        matched_skills = len(
            set(required_skills)
            &
            set(scholar_skill_names)
        )

        skills_score = 0

        if required_skills:
            skills_score = (
                matched_skills /
                len(required_skills)
            ) * 40

        # --------------------
        # Projects Score (20)
        # --------------------

        projects = db.query(
            Project
        ).filter(
            Project.user_id == scholar.user_id
        ).all()

        projects_score = min(
            len(projects) * 5,
            20
        )

        # --------------------
        # Achievement Score (10)
        # --------------------

        achievements = db.query(
            Achievement
        ).filter(
            Achievement.user_id == scholar.user_id
        ).all()

        achievement_score = min(
            len(achievements) * 2,
            10
        )

        # --------------------
        # Course Score (10)
        # --------------------

        course_score = 0

        if scholar.course:
            course_score = 10

        # --------------------
        # CGPA Score (10)
        # --------------------

        cgpa_score = 0

        try:

            cgpa = float(
                scholar.cgpa
            )

            cgpa_score = (
                min(cgpa, 10) / 10
            ) * 10

        except:
            pass

        # --------------------
        # Resume Score (10)
        # --------------------

        resume = db.query(
            Resume
        ).filter(
            Resume.user_id == scholar.user_id
        ).first()

        resume_score = 0

        if resume:
            resume_score = 10

        # --------------------
        # Final Score
        # --------------------

        score = int(
            skills_score
            + projects_score
            + achievement_score
            + course_score
            + cgpa_score
            + resume_score
        )

        results.append(
            {
                "scholar_id": scholar.id,
                "full_name": scholar.full_name,
                "match_score": score,
                "skills_score": round(skills_score, 2),
                "projects_score": round(projects_score, 2),
                "achievement_score": round(achievement_score, 2),
                "course_score": round(course_score, 2),
                "cgpa_score": round(cgpa_score, 2),
                "resume_score": round(resume_score, 2)
            }
        )

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.database.dependencies import get_db

# Models
from app.models.resume import Resume
from app.models.skill import Skill
from app.models.scholar import Scholar
from app.models.opportunity import Opportunity
from app.models.recommendation import Recommendation
from app.models.recommendation_feedback import RecommendationFeedback
from app.models.application import Application
from app.models.scholarship import Scholarship
from app.models.growth_metric import GrowthMetric

# Services
from app.services.gemini_service import (
    extract_skills,
    career_suggestions
)

from app.services.recommendation_service import (
    generate_recommendations
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/test")
def test_ai():
    return {
        "message": "AI Working"
    }


@router.post("/extract-resume/{user_id}")
def extract_resume_skills(
    user_id: int,
    db: Session = Depends(get_db)
):

    resume = db.query(Resume).filter(
        Resume.user_id == user_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    try:
        reader = PdfReader(
            resume.file_path
        )

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF Read Error: {str(e)}"
        )

    skills_text = extract_skills(
        resume_text
    )

    old_skills = db.query(Skill).filter(
        Skill.user_id == user_id
    ).all()

    for skill in old_skills:
        db.delete(skill)

    skill_list = skills_text.replace(
        "[", ""
    ).replace(
        "]", ""
    ).replace(
        "'", ""
    ).replace(
        '"', ""
    ).split(",")

    saved_skills = []

    for skill_name in skill_list:

        skill_name = skill_name.strip()

        if not skill_name:
            continue

        skill = Skill(
            user_id=user_id,
            skill_name=skill_name
        )

        db.add(skill)

        saved_skills.append(
            skill_name
        )

    db.commit()

    try:
        recommend(
        user_id=user_id,
        db=db
    )
    except:
        pass

    return {
        "message": "Skills Extracted",
        "skills": saved_skills
    }

@router.get("/skills/{user_id}")
def get_skills(
    user_id: int,
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).filter(
        Skill.user_id == user_id
    ).all()

    return skills

@router.get("/profile-score/{user_id}")
def profile_score(
    user_id: int,
    db: Session = Depends(get_db)
):

    scholar = db.query(Scholar).filter(
        Scholar.user_id == user_id
    ).first()

    if not scholar:
        raise HTTPException(
            status_code=404,
            detail="Scholar not found"
        )

    filled = 0
    missing = []

    fields = {
        "full_name": scholar.full_name,
        "phone": scholar.phone,
        "country": scholar.country,
        "university": scholar.university,
        "course": scholar.course,
        "academic_year": scholar.academic_year,
        "cgpa": scholar.cgpa,
        "bio": scholar.bio,

        "github_url": scholar.github_url,
        "portfolio_url": scholar.portfolio_url,
        "linkedin_url": scholar.linkedin_url,
        "project_links": scholar.project_links
    }

    for key, value in fields.items():

        if value:
            filled += 1
        else:
            missing.append(key)

    resume = db.query(
        Resume
    ).filter(
        Resume.user_id == user_id
    ).first()

    if resume:
        filled += 1
    else:
        missing.append("resume")

    skills = db.query(
        Skill
    ).filter(
        Skill.user_id == user_id
    ).all()

    if skills:
        filled += 1
    else:
        missing.append("skills")

    total_fields = 14

    score = int(
        (filled / total_fields) * 100
    )

    suggestions = [
        f"Add {item}"
        for item in missing
    ]

    return {
        "completion_score": score,
        "filled_fields": filled,
        "total_fields": total_fields,
        "missing_fields": missing,
        "suggestions": suggestions
    }

@router.post("/recommend/{user_id}")
def recommend(
    user_id: int,
    db: Session = Depends(get_db)
):

    profile = db.query(Scholar).filter(
        Scholar.user_id == user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Scholar profile not found"
        )

    skills = db.query(Skill).filter(
        Skill.user_id == user_id
    ).all()

    opportunities = db.query(
        Opportunity
    ).all()

    if not opportunities:
        raise HTTPException(
            status_code=404,
            detail="No opportunities found"
        )

    skill_names = [
        skill.skill_name
        for skill in skills
    ]

    recommendations = []

    db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).delete()

    for opportunity in opportunities:

        result = generate_recommendations(
            profile=profile,
            skills=skill_names,
            opportunity=opportunity
        )

        recommendation = Recommendation(
            user_id=user_id,
            opportunity_id=opportunity.id,
            relevance_score=result["score"],
            reason=result["reason"],
            status="recommended"
        )

        db.add(recommendation)

        if result["score"] >= 90:
            match_level = "Excellent Match"

        elif result["score"] >= 75:
            match_level = "Good Match"

        elif result["score"] >= 60:
            match_level = "Average Match"

        else:
            match_level = "Low Match"


        recommendations.append({
             "opportunity_id": opportunity.id,
             "title": opportunity.title,
             "score": result["score"],
             "match_level": match_level,
             "reason": result["reason"]
        })

    db.commit()

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "message": "Recommendations Generated",
        "user_id": user_id,
        "recommendations": recommendations
    }

@router.get("/recommendations/{user_id}")
def get_recommendations(
    user_id: int,
    db: Session = Depends(get_db)
):

    recommendations = db.query(
        Recommendation
    ).filter(
        Recommendation.user_id == user_id
    ).all()

    result = []

    for rec in recommendations:

        opportunity = db.query(
            Opportunity
        ).filter(
            Opportunity.id ==
            rec.opportunity_id
        ).first()

        result.append({
            "recommendation_id": rec.id,
            "title": opportunity.title if opportunity else None,
            "score": rec.relevance_score,
            "reason": rec.reason,
            "status": rec.status
        })

    return result

@router.get("/recommendation-stats/{user_id}")
def recommendation_stats(
    user_id: int,
    db: Session = Depends(get_db)
):

    recommendations = db.query(
        Recommendation
    ).filter(
        Recommendation.user_id == user_id
    ).all()

    total = len(recommendations)

    accepted = 0
    saved = 0
    rejected = 0

    for recommendation in recommendations:

        feedback = db.query(
            RecommendationFeedback
        ).filter(
            RecommendationFeedback.recommendation_id
            == recommendation.id
        ).first()

        if not feedback:
            continue

        if feedback.feedback == "accepted":
            accepted += 1

        elif feedback.feedback == "saved":
            saved += 1

        elif feedback.feedback == "rejected":
            rejected += 1

    return {
        "total_recommendations": total,
        "accepted": accepted,
        "saved": saved,
        "rejected": rejected
    }

@router.post("/feedback")
def submit_feedback(
    recommendation_id: int,
    feedback: str,
    db: Session = Depends(get_db)
):

    allowed_feedback = [
        "accepted",
        "saved",
        "rejected"
    ]

    if feedback not in allowed_feedback:
        raise HTTPException(
            status_code=400,
            detail="Feedback must be accepted, saved or rejected"
        )

    recommendation = db.query(
        Recommendation
    ).filter(
        Recommendation.id == recommendation_id
    ).first()

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    existing = db.query(
        RecommendationFeedback
    ).filter(
        RecommendationFeedback.recommendation_id
        == recommendation_id
    ).first()

    if existing:

        existing.feedback = feedback

    else:

        new_feedback = RecommendationFeedback(
            recommendation_id=recommendation_id,
            feedback=feedback
        )

        db.add(new_feedback)

    if feedback == "accepted":
        recommendation.relevance_score += 15

    elif feedback == "saved":
        recommendation.relevance_score += 5

    elif feedback == "rejected":
        recommendation.relevance_score -= 20

    recommendation.relevance_score = max(
        0,
        min(recommendation.relevance_score, 100)
    )

    db.commit()

    return {
        "message": "Feedback Saved",
        "new_score": recommendation.relevance_score
    }


@router.get("/career-suggestions/{user_id}")
def get_career_suggestions(
    user_id: int,
    db: Session = Depends(get_db)
):

    profile = db.query(
        Scholar
    ).filter(
        Scholar.user_id == user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Scholar profile not found"
        )

    skills = db.query(
        Skill
    ).filter(
        Skill.user_id == user_id
    ).all()

    skill_names = [
        skill.skill_name
        for skill in skills
    ]

    result = career_suggestions(
        profile,
        skill_names
    )

    return {
        "user_id": user_id,
        "suggestions": result
    }
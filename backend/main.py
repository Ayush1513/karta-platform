from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.user import User
from app.models.scholar import Scholar
from app.models.approved_scholar import ApprovedScholar
from app.models.approved_organization import (ApprovedOrganization)
from app.models.password_reset_otp import PasswordResetOTP
from app.models.scholarship import Scholarship
from app.models.application import Application
from app.models.resume import Resume
from app.models.skill import Skill
from app.models.project import Project
from app.models.achievement import Achievement
from app.models.achievement_save import AchievementSave
from app.models.organization import Organization
from app.models.opportunity import Opportunity
from app.models.recommendation import Recommendation
from app.models.recommendation_feedback import RecommendationFeedback
from app.models.growth_metric import GrowthMetric
from app.models.connection import Connection
from app.models.message import Message
from app.models.organization_invite import OrganizationInvite
from app.models.report import Report

from app.api.auth import router as auth_router
from app.api.scholar import router as scholar_router
from app.api.approved_scholar import (router as approved_scholar_router)
from app.api.approved_organization import (router as approved_organization_router)
from app.api.scholarship import router as scholarship_router
from app.api.application import router as application_router
from app.api.dashboard import router as dashboard_router
from app.api.resume import router as resume_router
from app.api.ai import router as ai_router
from app.api.project import router as project_router
from app.api.achievement import router as achievement_router
from app.models.achievement_like import AchievementLike
from app.models.achievement_comment import AchievementComment
from app.api.opportunity import router as opportunity_router
from app.api.organization import router as organization_router
from app.api.connection import router as connection_router
from app.api.message import router as message_router
from app.api.admin import router as admin_router
from app.api.report import router as report_router
from app.api.admin_ai import router as admin_ai_router
from app.api.notification import router as notification_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Karta Platform",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(scholar_router)
app.include_router(approved_scholar_router)
app.include_router(approved_organization_router)
app.include_router(scholarship_router)
app.include_router(application_router)
app.include_router(dashboard_router)
app.include_router(resume_router)
app.include_router(opportunity_router)
app.include_router(ai_router)
app.include_router(project_router)
app.include_router(achievement_router)
app.include_router(organization_router)
app.include_router(connection_router)
app.include_router(message_router)
app.include_router(admin_router)
app.include_router(report_router)
app.include_router(admin_ai_router)
app.include_router(notification_router)

@app.get("/")
def root():
    return {
        "message": "Karta Platform Running"
    } 
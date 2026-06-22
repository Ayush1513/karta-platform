from pydantic import BaseModel
from typing import Optional

class AchievementCreate(BaseModel):
    title: str
    description: str
    achievement_type: str
    image_url: Optional[str] = None
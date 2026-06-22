from pydantic import BaseModel


class ScholarMatchResponse(BaseModel):
    scholar_id: int
    full_name: str
    match_score: int
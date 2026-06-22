from pydantic import BaseModel


class ProjectCreate(BaseModel):

    title: str

    description: str

    tech_stack: str

    github_url: str | None = None

    live_url: str | None = None

    is_pinned: bool = False
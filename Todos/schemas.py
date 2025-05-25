from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=2)
    priority: int = Field(gt=0, lt=6)
    completed: bool = Field(default=False)

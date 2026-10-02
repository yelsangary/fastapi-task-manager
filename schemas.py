from pydantic import BaseModel, Field, field_validator
from typing import Literal

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    priority: Literal["low", "medium", "high"]
    description: str = Field(default="No description")

    @field_validator('title')
    @classmethod
    def check_upper_case(cls, v):
        if not v[0].isupper():
            raise ValueError("Title must start with an uppercase letter")
        return v

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=50)
    priority: Literal["low", "medium", "high"] | None = None
    description: str | None = None

    @field_validator('title')
    @classmethod
    def check_upper(cls, v):
        if v is not None and not v[0].isupper():
            raise ValueError("Title must start with an uppercase letter")
        return v

class TaskResponse(BaseModel):
    task_id: int
    title: str
    priority: str
    description: str
    status: str
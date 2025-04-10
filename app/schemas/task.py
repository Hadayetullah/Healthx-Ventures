from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
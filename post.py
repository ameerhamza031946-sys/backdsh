from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str = Field(..., title="Title of the post", min_length=1, max_length=100)
    content: str = Field(..., title="Content of the post", min_length=1)

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostResponse(PostBase):
    id: str
    owner_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

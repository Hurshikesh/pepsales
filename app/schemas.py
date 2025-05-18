from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    type: str
    content: str

class NotificationOut(BaseModel):
    id: int
    user_id: int
    type: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

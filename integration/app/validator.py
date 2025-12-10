from pydantic import BaseModel, Field, validator
from typing import Optional

class IncomingA(BaseModel):
    id: str = Field(..., description="external id from A")
    name: str
    phone: Optional[str] = None
    joined_at: Optional[str] = None

    @validator("name")
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("name required")
        return v.strip()

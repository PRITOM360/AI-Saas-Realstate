from pydantic import BaseModel
from datetime import datetime


class TenantCreate(BaseModel):
    name: str
    subdomain: str


class TenantResponse(BaseModel):
    id: int
    name: str
    subdomain: str
    created_at: datetime

    class Config:
        from_attributes = True
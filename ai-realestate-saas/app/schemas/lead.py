from pydantic import BaseModel
from datetime import datetime


class LeadCreate(BaseModel):
    name: str
    phone: str


class LeadReplyRequest(BaseModel):
    message: str


class LeadResponse(BaseModel):
    id: int
    name: str
    phone: str
    score: int
    status: str
    created_at: datetime
    tenant_id: int

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    sender: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True


class AppointmentResponse(BaseModel):
    id: int
    lead_id: int
    scheduled_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True
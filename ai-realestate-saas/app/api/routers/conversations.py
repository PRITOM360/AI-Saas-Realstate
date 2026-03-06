from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db import models
from app.schemas.lead import ConversationResponse
from app.api.deps import get_current_tenant

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("/{lead_id}", response_model=List[ConversationResponse])
def get_conversations(
    lead_id: int,
    db: Session = Depends(get_db),
    tenant: models.Tenant = Depends(get_current_tenant),
):
    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id,
        models.Lead.tenant_id == tenant.id
    ).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    conversations = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.lead_id == lead_id,
            models.Conversation.tenant_id == tenant.id
        )
        .order_by(models.Conversation.timestamp.asc())
        .all()
    )
    return conversations
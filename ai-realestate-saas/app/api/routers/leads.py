from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db import models
from app.schemas.lead import LeadCreate, LeadResponse, LeadReplyRequest
from app.api.deps import get_current_tenant
from app.services.lead_service import process_message
from app.services.booking_service import create_appointment_if_needed

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("", response_model=LeadResponse)
def create_lead(
    lead_in: LeadCreate,
    db: Session = Depends(get_db),
    tenant: models.Tenant = Depends(get_current_tenant),
):
    new_lead = models.Lead(
        tenant_id=tenant.id,
        name=lead_in.name,
        phone=lead_in.phone,
        score=0,
        status="cold",
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    first_message = models.Conversation(
        tenant_id=tenant.id,
        lead_id=new_lead.id,
        message=f"Hi {lead_in.name}, are you currently looking to buy a home?",
        sender="ai",
    )
    db.add(first_message)
    db.commit()

    return new_lead


@router.get("", response_model=List[LeadResponse])
def get_all_leads(
    db: Session = Depends(get_db),
    tenant: models.Tenant = Depends(get_current_tenant),
):
    leads = db.query(models.Lead).filter(models.Lead.tenant_id == tenant.id).all()
    return leads


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
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
    return lead


@router.post("/{lead_id}/reply")
def reply_to_lead(
    lead_id: int,
    payload: LeadReplyRequest,
    db: Session = Depends(get_db),
    tenant: models.Tenant = Depends(get_current_tenant),
):
    lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id,
        models.Lead.tenant_id == tenant.id
    ).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    ai_result = process_message(db, lead, payload.message)
    appointment_time = create_appointment_if_needed(db, lead, ai_result)

    return {
        "lead_id": lead.id,
        "updated_score": lead.score,
        "updated_status": lead.status,
        "booking_triggered": appointment_time is not None,
        "ai_reply": ai_result.get("reply", ""),
    }
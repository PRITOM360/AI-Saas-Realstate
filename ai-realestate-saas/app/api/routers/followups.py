from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.api.deps import get_current_tenant
from app.services.followup_service import generate_followup

router = APIRouter(prefix="/followups", tags=["Followups"])


@router.post("/run")
def trigger_followups(
    db: Session = Depends(get_db),
    tenant: models.Tenant = Depends(get_current_tenant),
):
    leads = db.query(models.Lead).filter(models.Lead.tenant_id == tenant.id).all()
    triggered = []

    for lead in leads:
        reply = generate_followup(db, lead)
        triggered.append({"lead_id": lead.id, "message": reply})

    return {"followups_triggered": triggered}
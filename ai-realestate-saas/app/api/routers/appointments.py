from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db import models
from app.schemas.lead import AppointmentResponse
from app.api.deps import get_current_tenant

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("", response_model=List[AppointmentResponse])
def get_appointments(
    db: Session = Depends(get_db),
    tenant: models.Tenant = Depends(get_current_tenant),
):
    appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.tenant_id == tenant.id)
        .all()
    )
    return appointments
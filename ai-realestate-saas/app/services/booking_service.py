from datetime import datetime, timedelta

from app.db.models import Appointment


def create_appointment_if_needed(
    db,
    lead,
    ai_result
):

    if not ai_result.get("booking"):
        return None

    appointment_time = datetime.utcnow() + timedelta(days=1)

    appointment = Appointment(
        tenant_id=lead.tenant_id,
        lead_id=lead.id,
        scheduled_time=appointment_time
    )

    db.add(appointment)

    lead.status = "appointment_scheduled"

    db.commit()

    return appointment_time
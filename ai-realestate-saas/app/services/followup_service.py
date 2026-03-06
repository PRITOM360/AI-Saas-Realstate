from app.ai.client import ask_ai
from app.db.models import Conversation


def generate_followup(db, lead):

    prompt = f"Write a short follow up SMS for a {lead.status} real estate buyer."

    ai_reply = ask_ai(prompt)

    followup = Conversation(
        tenant_id=lead.tenant_id,
        lead_id=lead.id,
        message=ai_reply,
        sender="ai"
    )

    db.add(followup)

    db.commit()

    return ai_reply
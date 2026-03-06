import json

from app.ai.client import ask_ai
from app.db.models import Conversation
from app.utils.logger import logger


def process_message(db, lead, user_message):

    user_convo = Conversation(
        tenant_id=lead.tenant_id,
        lead_id=lead.id,
        message=user_message,
        sender="user"
    )

    db.add(user_convo)
    db.commit()

    ai_raw = ask_ai(user_message)

    try:
        ai_data = json.loads(ai_raw)

    except json.JSONDecodeError:

        logger.error("AI JSON parsing failed")

        ai_data = {
            "reply": "Thanks. Our agent will contact you.",
            "score": lead.score,
            "status": lead.status,
            "booking": False
        }

    lead.score = ai_data.get("score", lead.score)

    lead.status = ai_data.get("status", lead.status)

    db.commit()

    ai_convo = Conversation(
        tenant_id=lead.tenant_id,
        lead_id=lead.id,
        message=ai_data.get("reply"),
        sender="ai"
    )

    db.add(ai_convo)

    db.commit()

    return ai_data
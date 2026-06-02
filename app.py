from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from services.openai_service import generate_response
from services.lead_memory import get_lead, update_lead

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):

    form = await request.form()

    user_msg = form.get("Body")
    from_number = form.get("From")
    user_id = from_number

    # 🧠 Get or create lead memory
    lead = get_lead(user_id)

    # 🧠 Simple memory extraction
    msg_lower = user_msg.lower()

    if "budget" in msg_lower:
        update_lead(user_id, "budget", user_msg)

    if "investment" in msg_lower:
        update_lead(user_id, "purpose", "investment")

    if "personal" in msg_lower:
        update_lead(user_id, "purpose", "personal")

    # 🧠 Build AI context with memory
    context = f"""
You are a professional Dubai real estate assistant.

You MUST use the user memory:
- Budget: {lead.get('budget')}
- Purpose: {lead.get('purpose')}
- Interest: {lead.get('interest')}

Rules:
- Do NOT repeat questions already answered
- Ask only missing important details
- Focus on qualifying the lead for property viewing in Dubai

User message:
{user_msg}
"""

    # 🤖 Generate AI response
    ai_reply = generate_response(context)

    # 📩 Send WhatsApp response (FIXED XML ISSUE)
    response = MessagingResponse()
    response.message(ai_reply)

    return Response(str(response), media_type="application/xml")
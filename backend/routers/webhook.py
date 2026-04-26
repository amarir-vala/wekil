# backend/routers/webhook.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.llm import get_ai_reply

router = APIRouter()

# This defines the shape of the incoming request
class MessageRequest(BaseModel):
    shop_name: str
    customer_message: str

@router.post("/message")
def handle_message(request: MessageRequest):
    """
    Receives a customer message, returns AI reply.
    Later: this will be triggered by WhatsApp webhook.
    """
    reply = get_ai_reply(
        user_message=request.customer_message,
        shop_name=request.shop_name
    )

    return {
        "shop": request.shop_name,
        "customer_said": request.customer_message,
        "ai_replied": reply
    }
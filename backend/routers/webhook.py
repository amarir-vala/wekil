# backend/routers/webhook.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.llm import get_ai_reply
from backend.services.rag import add_catalog_items

router = APIRouter()

class MessageRequest(BaseModel):
    shop_id: str
    shop_name: str
    customer_phone: str    
    customer_message: str

class CatalogRequest(BaseModel):
    shop_id: str
    items: list[dict]

@router.post("/catalog")
def upload_catalog(request: CatalogRequest):
    result = add_catalog_items(shop_id=request.shop_id, items=request.items)
    return {"status": "catalog uploaded", "items_added": result["added"]}

@router.post("/message")
def handle_message(request: MessageRequest):
    reply = get_ai_reply(
        user_message=request.customer_message,
        shop_name=request.shop_name,
        shop_id=request.shop_id,
        customer_phone=request.customer_phone
    )
    return {
        "shop": request.shop_name,
        "customer_said": request.customer_message,
        "ai_replied": reply
    }
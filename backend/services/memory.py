# backend/services/memory.py
from supabase import create_client
from backend.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_message(shop_id: str, customer_phone: str, role: str, content: str):
    """Save a single message to Supabase."""
    supabase.table("conversations").insert({
        "shop_id": shop_id,
        "customer_phone": customer_phone,
        "role": role,        # "user" or "assistant"
        "content": content
    }).execute()

def load_history(shop_id: str, customer_phone: str, limit: int = 10) -> list:
    """
    Load last N messages for this customer in this shop.
    Returns them in the format Groq expects.
    """
    response = (
        supabase.table("conversations")
        .select("role, content")
        .eq("shop_id", shop_id)
        .eq("customer_phone", customer_phone)
        .order("created_at", desc=False)
        .limit(limit)
        .execute()
    )

    # Format for Groq: [{"role": "user", "content": "..."}, ...]
    return [
        {"role": row["role"], "content": row["content"]}
        for row in response.data
    ]
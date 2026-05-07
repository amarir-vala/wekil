# backend/services/llm.py
from groq import Groq
from backend.config import GROQ_API_KEY
from backend.services.rag import retrieve_context
from backend.services.memory import save_message, load_history

client = Groq(api_key=GROQ_API_KEY)

def get_ai_reply(
    user_message: str,
    shop_name: str,
    shop_id: str,
    customer_phone: str
) -> str:

    # 1. Retrieve relevant catalog info
    context = retrieve_context(shop_id=shop_id, query=user_message)

    # 2. Load conversation history
    history = load_history(shop_id=shop_id, customer_phone=customer_phone)

    # 3. Build system prompt
    system_prompt = f"""You are a helpful customer service assistant for {shop_name}.
Reply in the same language the customer uses.
If they write in Arabic or Darija, reply in Arabic.
If they write in French, reply in French.
Be friendly, concise, and helpful.

Use ONLY the information below to answer.
If the answer is not in the information, say you don't have that info.

Shop catalog:
{context}"""

    # 4. Build full message list: history + new message
    messages = [
        {"role": "system", "content": system_prompt},
        *history,                                        # ← past messages
        {"role": "user", "content": user_message}        # ← current message
    ]

    # 5. Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    reply = response.choices[0].message.content

    # 6. Save both messages to Supabase
    save_message(shop_id, customer_phone, "user", user_message)
    save_message(shop_id, customer_phone, "assistant", reply)

    return reply
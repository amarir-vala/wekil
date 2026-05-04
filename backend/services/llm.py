# backend/services/llm.py
from groq import Groq
from backend.config import GROQ_API_KEY
from backend.services.rag import retrieve_context

client = Groq(api_key=GROQ_API_KEY)

def get_ai_reply(user_message: str, shop_name: str, shop_id: str) -> str:
    
    # 🔍 Retrieve relevant catalog info
    context = retrieve_context(shop_id=shop_id, query=user_message)

    # 📋 Build system prompt with real context
    system_prompt = f"""You are a helpful customer service assistant for {shop_name}.
Reply in the same language the customer uses.
If they write in Arabic or Darija, reply in Arabic.
If they write in French, reply in French.
Be friendly, concise, and helpful.

Use ONLY the information below to answer. 
If the answer is not in the information, say you don't have that info.

Shop catalog:
{context}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content
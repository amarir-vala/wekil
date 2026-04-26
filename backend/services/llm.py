# backend/services/llm.py
from groq import Groq
from backend.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def get_ai_reply(user_message: str, shop_name: str = "the shop") -> str:
    """
    Takes a customer message and returns an AI reply.
    This will later include RAG context and conversation history.
    """
    
    system_prompt = f"""You are a helpful customer service assistant for {shop_name}.
You reply in the same language the customer uses.
If they write in Arabic or Darija, reply in Arabic.
If they write in French, reply in French.
Be friendly, concise, and helpful."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Best free model on Groq
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content
# backend/services/rag.py
import chromadb
from sentence_transformers import SentenceTransformer

# Load a multilingual model — handles Arabic + French + English
embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Initialize ChromaDB (stores data locally in .chroma/ folder)
chroma_client = chromadb.PersistentClient(path=".chroma")

def get_or_create_collection(shop_id: str):
    """Each shop gets its own collection (its own knowledge base)."""
    return chroma_client.get_or_create_collection(name=f"shop_{shop_id}")

def add_catalog_items(shop_id: str, items: list[dict]):
    """
    Upload catalog items to ChromaDB.
    Each item: {"id": "1", "text": "Red djellaba - 350 MAD, sizes S/M/L"}
    """
    collection = get_or_create_collection(shop_id)

    ids = [item["id"] for item in items]
    texts = [item["text"] for item in items]

    # Convert texts to vectors (embeddings)
    embeddings = embedder.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings
    )
    return {"added": len(items)}

def retrieve_context(shop_id: str, query: str, top_k: int = 3) -> str:
    """
    Given a customer question, find the most relevant catalog items.
    Returns them as a single string to inject into the AI prompt.
    """
    collection = get_or_create_collection(shop_id)

    # Convert the question to a vector
    query_embedding = embedder.encode([query]).tolist()

    # Search for top_k most similar items
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    # Join results into one context string
    docs = results["documents"][0]
    return "\n".join(docs) if docs else ""
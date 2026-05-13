# backend/services/rag.py
import chromadb

# ⚠️ Don't load at startup — load on first use
_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _embedder

chroma_client = chromadb.PersistentClient(path=".chroma")

def get_or_create_collection(shop_id: str):
    return chroma_client.get_or_create_collection(name=f"shop_{shop_id}")

def add_catalog_items(shop_id: str, items: list[dict]):
    collection = get_or_create_collection(shop_id)
    embedder = get_embedder()
    ids = [item["id"] for item in items]
    texts = [item["text"] for item in items]
    embeddings = embedder.encode(texts).tolist()
    collection.add(ids=ids, documents=texts, embeddings=embeddings)
    return {"added": len(items)}

def retrieve_context(shop_id: str, query: str, top_k: int = 3) -> str:
    collection = get_or_create_collection(shop_id)
    embedder = get_embedder()
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    docs = results["documents"][0]
    return "\n".join(docs) if docs else ""
# app/rag/vector_store.py
import faiss
import pickle
import numpy as np
import os
from app.ingestion.chunker import all_docs

INDEX_FILE = os.path.join(os.path.dirname(__file__), "faiss_index.pkl")
METADATA_FILE = os.path.join(os.path.dirname(__file__), "metadata.pkl")

def build_faiss_index():
    # Dummy embeddings using sentence-transformers or any embedding model
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    texts = [doc["text"] for doc in all_docs]
    embeddings = model.encode(texts, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and metadata
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(all_docs, f)

    print(f"Built FAISS index with {len(all_docs)} chunks.")
    return index, all_docs

def load_faiss_index():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(METADATA_FILE):
        raise FileNotFoundError("FAISS index not found. Build it first using build_faiss_index().")
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "rb") as f:
        metadata_list = pickle.load(f)
    return index, metadata_list

# If you run this file directly, build the index
if __name__ == "__main__":
    build_faiss_index()
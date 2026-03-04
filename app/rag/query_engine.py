# app/rag/query_engine.py

import ollama
import numpy as np
from app.rag.vector_store import load_faiss_index  # Make sure you have this function
from app.ingestion.chunker import all_docs  # now works
from sentence_transformers import SentenceTransformer


# --------------------------
# Load FAISS index and metadata
# --------------------------
index, metadata = load_faiss_index()  # Should return FAISS index and metadata list

# --------------------------
# Query function
# --------------------------





# Load FAISS index + metadata


# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def query_bot(user_query, top_k=3):
    # Step 1: Convert user query to embedding
    query_vector = embed_model.encode([user_query], convert_to_numpy=True)

    # Step 2: Retrieve top-K chunks from FAISS
    D, I = index.search(query_vector, top_k)

    # Step 3: Build context from top-K chunks
    context = ""
    for idx in I[0]:
        context += metadata[idx]["text"] + "\n"

    print("TOP-K CONTEXT:\n", context)
    context = context[:2000] 
    print("TOP-K CONTEXT:\n", context)  

    # Step 4: Build prompt


    prompt = f"""You are an assistant for TechBridge Sol company.
    Answer the user's question based ONLY on the context below.
    If the answer is not in the context, say 'Information not found.'

    Context:
    {context}

    Question:
    {user_query}

    Answer:
    """

    # Step 5: Call Ollama with system + user messages
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are a helpful company assistant."},
            {"role": "user", "content": prompt}
        ]
    )






    """prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {user_query}\nAnswer:"

    # Step 5: Call Ollama LLM
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )"""

    # Step 6: Extract answer safely
    print("RAW RESPONSE:\n", response)

    try:
        return response.message.content
    except Exception:
        return ""


# --------------------------
# CLI loop
# --------------------------
if __name__ == "__main__":
    print("Company Knowledge Bot (type 'exit' to quit)")
    while True:
        q = input("Ask your question: ")
        if q.lower() in ["exit", "quit"]:
            break
        ans = query_bot(q)
        print("\nAnswer:\n", ans)
        print("-" * 50)
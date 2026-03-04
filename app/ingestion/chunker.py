# app/ingestion/chunker.py
from app.ingestion.pdf_loader import all_docs

# Chunking parameters
chunk_size = 500  # characters per chunk
chunks = []

for doc in all_docs:
    text = doc["text"]
    for i in range(0, len(text), chunk_size):
        chunks.append({
            "file_name": doc["file_name"],
            "page_number": doc["page_number"],
            "text": text[i:i+chunk_size]
        })

# Expose chunked docs as all_docs
all_docs = chunks
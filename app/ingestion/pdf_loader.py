# app/ingestion/pdf_loader.py
import os
from pypdf import PdfReader

PDF_ROOT = os.path.join(os.path.dirname(__file__), "../../data")  # top-level data folder

all_docs = []

for root, dirs, files in os.walk(PDF_ROOT):
    for filename in files:
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(root, filename)
            reader = PdfReader(file_path)
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text:
                    all_docs.append({
                        "file_name": filename,
                        "page_number": page_number,
                        "text": text
                    })

print(f"Loaded {len(all_docs)} pages from {len(set([d['file_name'] for d in all_docs]))} PDF files.")
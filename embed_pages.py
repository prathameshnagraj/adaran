import os
import json
import torch
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Paths
CHUNKS_DIR = "chunking"
PERSIST_DIR = "chroma_db/pages"
os.makedirs(PERSIST_DIR, exist_ok=True)

def load_chunks():
    path = os.path.join(CHUNKS_DIR, "chunked_pages.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Missing: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    all_chunks = []
    for chunk in chunks:
        # ✅ Filter metadata to only str, int, float, bool
        metadata = {k: v for k, v in chunk.items() if k != "chunk_text" and isinstance(v, (str, int, float, bool))}
        
        doc = Document(
            page_content=chunk["chunk_text"],
            metadata=metadata
        )
        all_chunks.append(doc)

    return all_chunks

# Load chunks
documents = load_chunks()
print(f"📄 Loaded {len(documents)} webpage chunks for embedding.")

# Load embedding model
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Using device: {device}")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)

# Create and persist Chroma vectorstore
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=PERSIST_DIR,
    collection_name="pages"
)

vectorstore.persist()
print(f"✅ Vectorstore saved at: {PERSIST_DIR}")

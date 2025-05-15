import os
import torch
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder

# ChromaDB path
CHROMA_PATH = "chroma_db/pages"

# Load embedding model
device = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)

# Load reranker model
reranker = CrossEncoder('BAAI/bge-reranker-base', device=device)

# Load Chroma vectorstore
def load_vectorstore():
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(f"❌ ChromaDB not found at {CHROMA_PATH}")
    
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model,
        collection_name="pages"
    )
    print(f"✅ Vectorstore loaded from {CHROMA_PATH}")
    return vectorstore

# Rerank documents based on query
def rerank_documents(query, docs, top_n=1):
    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)

    scored_docs = list(zip(docs, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)  # Highest first

    top_docs = [doc for doc, score in scored_docs[:top_n]]
    return top_docs

# Combined retrieval + rerank function
def retrieve_documents(query, k_retrieve=10, k_rerank=5):
    vs = load_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": k_retrieve})
    rough_docs = retriever.get_relevant_documents(query)

    print(f"🔍 Retrieved {len(rough_docs)} rough documents for query: '{query}'")

    final_docs = rerank_documents(query, rough_docs, top_n=k_rerank)

    # Optional: Log metadata counts
    sitemap_counts = {}
    program_type_counts = {}
    for doc in final_docs:
        sitemap = doc.metadata.get("sitemap", "Unknown")
        program_type = doc.metadata.get("program_type", "Unknown")

        sitemap_counts[sitemap] = sitemap_counts.get(sitemap, 0) + 1
        program_type_counts[program_type] = program_type_counts.get(program_type, 0) + 1

    print(f"📚 Sitemap counts: {sitemap_counts}")
    print(f"🎓 Program Type counts: {program_type_counts}")

    return final_docs

if __name__ == "__main__":
    query = "Tell me about the MS Accounting admission process."
    top_docs = retrieve_documents(query)

    for i, doc in enumerate(top_docs):
        print(f"\nChunk {i+1}:")
        print(f"Source URL: {doc.metadata.get('source_url')}")
        print(f"Chunk Text: {doc.page_content[:300]}...")

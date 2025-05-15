import json
import os
import nltk
from typing import List

# Download punkt tokenizer if not already present
nltk.download('punkt')

def load_tagged_pages(filepath: str) -> List[dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_chunked_pages(chunks: List[dict], filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

def chunk_sentences(sentences: List[str], chunk_size: int = 800, overlap_sentences: int = 2) -> List[List[str]]:
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        
        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            # Save current chunk
            chunks.append(current_chunk)

            # Start new chunk with overlap
            overlap = current_chunk[-overlap_sentences:] if len(current_chunk) >= overlap_sentences else current_chunk
            current_chunk = overlap + [sentence]
            current_length = sum(len(s) for s in current_chunk)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def chunk_texts(data: List[dict], chunk_size: int = 800, overlap_sentences: int = 2) -> List[dict]:
    all_chunks = []
    
    for entry in data:
        source_url = entry.get('source_url', '')
        sitemap = entry.get('sitemap', '')
        program_type = entry.get('program_type', '')
        slugs = entry.get('slugs', [])
        full_text = entry.get('text', '')

        if not full_text.strip():
            continue  # Skip empty entries

        sentences = nltk.sent_tokenize(full_text)
        sentence_chunks = chunk_sentences(sentences, chunk_size, overlap_sentences)

        for i, sentence_group in enumerate(sentence_chunks):
            chunk_text = " ".join(sentence_group)
            chunked_entry = {
                "source_url": source_url,
                "sitemap": sitemap,
                "program_type": program_type,
                "slugs": slugs,
                "chunk_text": chunk_text,
                "chunk_id": f"{source_url}#chunk-{i}"
            }
            all_chunks.append(chunked_entry)

    return all_chunks

if __name__ == "__main__":
    input_path = "data_cleaned/tagged_pages.json"
    output_path = "chunking/chunked_pages.json"
    
    if not os.path.exists("chunking"):
        os.makedirs("chunking")

    print("📦 Loading tagged pages...")
    tagged_data = load_tagged_pages(input_path)
    
    print("✂️ Splitting into sentence-aware chunks using NLTK...")
    chunked_data = chunk_texts(tagged_data)

    print(f"✅ Total chunks created: {len(chunked_data)}")
    save_chunked_pages(chunked_data, output_path)
    print(f"✅ Chunked pages saved to {output_path}")

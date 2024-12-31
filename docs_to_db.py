import json
import os
import tiktoken 
from sentence_transformers import SentenceTransformer
import chromadb
import time

JSON_PATH = "manim-docs/docs.manim.community/manim_docs.json"

def chunk_text_tiktoken(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of ~chunk_size tokens using tiktoken.
    Overlaps each chunk by 'overlap' tokens for context continuity.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []

    idx = 0
    while idx < len(tokens):
        end = idx + chunk_size
        chunk_slice = tokens[idx:end]
        chunk_str = encoding.decode(chunk_slice)
        chunks.append(chunk_str)
        idx += chunk_size - overlap

    return chunks

def batch_iterable(iterable, batch_size):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]

def main():
    print("Current Working Directory:", os.getcwd())
    
    print("Initializing ChromaDB...")
    chroma_path = "./chroma_db"
    client = chromadb.PersistentClient(path=chroma_path)
    
    try:
        heartbeat = client.heartbeat()
        print(f"ChromaDB connected successfully. Heartbeat: {heartbeat}")
    except Exception as e:
        print(f"Failed to connect to ChromaDB: {str(e)}")
        return

    # Load the Manim docs from JSON
    if not os.path.isfile(JSON_PATH):
        print(f"ERROR: JSON file not found at {JSON_PATH}")
        return

    print("Loading JSON file...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        manim_docs = json.load(f)

    all_chunks = []

    print("Processing documents...")
    for doc in manim_docs:
        file_path = doc.get("file_path", "unknown_path")
        text_content = doc.get("text", "")
        code_blocks = doc.get("code_blocks", [])

        # Chunk the main text
        text_chunks = chunk_text_tiktoken(text_content, chunk_size=500, overlap=50)
        for i, chunk_str in enumerate(text_chunks):
            all_chunks.append({
                "source": file_path,
                "chunk_id": f"text_{i}",
                "content": chunk_str
            })

        # Chunk the code blocks
        for j, code_block_text in enumerate(code_blocks):
            code_chunks = chunk_text_tiktoken(code_block_text, chunk_size=300, overlap=30)
            for k, chunk_str in enumerate(code_chunks):
                all_chunks.append({
                    "source": file_path,
                    "chunk_id": f"code_{j}_{k}",
                    "content": chunk_str
                })

    print(f"Created {len(all_chunks)} total chunks.")

    # Create embeddings
    print("Creating embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts_for_embedding = [chunk["content"] for chunk in all_chunks]
    embeddings = model.encode(texts_for_embedding, show_progress_bar=True)

    # Create or get collection
    collection = client.get_or_create_collection("manim_docs")
    
    print("Preparing data for storage...")
    ids = [f"{chunk['source']}_{chunk['chunk_id']}" for chunk in all_chunks]
    docs = [chunk["content"] for chunk in all_chunks]
    metas = [{"source": chunk["source"], "chunk_id": chunk["chunk_id"]} for chunk in all_chunks]
    embs = [emb.tolist() for emb in embeddings]

    # Store data in batches
    print("Storing data in batches...")
    max_batch_size = 5460
    batch_count = 0
    for batch_ids, batch_docs, batch_metas, batch_embs in zip(
        batch_iterable(ids, max_batch_size),
        batch_iterable(docs, max_batch_size),
        batch_iterable(metas, max_batch_size),
        batch_iterable(embs, max_batch_size),
    ):
        collection.add(
            documents=batch_docs,
            embeddings=batch_embs,
            ids=batch_ids,
            metadatas=batch_metas
        )
        batch_count += 1
        print(f"Processed batch {batch_count}")
        
        client.heartbeat()

    print("\nVerifying storage...")
    try:
        collection_count = collection.count()
        print(f"Number of items in collection: {collection_count}")
        
        if collection_count > 0:
            results = collection.peek(limit=1)
            print(f"Sample document ID: {results['ids'][0]}")
            print(f"Sample document content (truncated): {results['documents'][0][:100]}...")
        
        print("\nChroma DB directory contents:")
        for root, dirs, files in os.walk(chroma_path):
            for file in files:
                print(f"File: {os.path.join(root, file)}")
                
        final_heartbeat = client.heartbeat()
        print(f"Final heartbeat check: {final_heartbeat}")
        
    except Exception as e:
        print(f"Error during verification: {str(e)}")

    print("All done!")

if __name__ == "__main__":
    main()
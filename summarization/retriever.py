from sentence-transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text):
    chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
    return chunks

def build_index(chunks):
    vectors = model.encode(chunks)
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors, dtype=np.float32))
    return index, vectors

def retrieve_relevant_chunks(keyword, chunks, index, top_k=3):
    keyword_vector = model.encode([keyword])
    distances, indices = index.search(np.array(keyword_vector, dtype=np.float32), top_k)
    relevant = [chunks[i] for i in indices[0] if i < len(chunks)]
    return relevant
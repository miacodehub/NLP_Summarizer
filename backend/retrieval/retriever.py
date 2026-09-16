from retrieval.embedder import embed_texts, embed_query
from retrieval.vector_store import VectorStore


class Retriever:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks

        texts = [chunk["text"] for chunk in chunks]

        embeddings = embed_texts(texts)

        dimension = embeddings.shape[1]

        self.vector_store = VectorStore(dimension)

        self.vector_store.add(
            embeddings,
            chunks
        )

    def search(self, query: str, k: int = 3):
        query_embedding = embed_query(query)

        return self.vector_store.search(
            query_embedding,
            k
        )
import faiss
import numpy as np

from config.config import SCORE_THRESHOLD


class VectorStore:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks = []

    def add(self, embeddings, chunks: list[str]):
        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding, k: int = 3):
        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            if score < SCORE_THRESHOLD:
                continue

            results.append({
                "chunk": self.chunks[index],
                "score": float(score)
            })

        return results
from retrieval.retriever import Retriever
from summarization.generator import generate_summary


class RAGPipeline:
    def __init__(self, chunks: list[dict]):
        self.retriever = Retriever(chunks)

    def answer(self, query: str, k: int = 3):
        results = self.retriever.search(query, k)

        if not results:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        # Group retrieved chunks by source filename instead of flattening
        # into one string — lets the generator summarize each source
        # independently (map step) before combining (reduce step).
        chunks_by_source: dict[str, str] = {}
        for result in results:
            filename = result["chunk"]["filename"]
            text = result["chunk"]["text"]
            if filename in chunks_by_source:
                chunks_by_source[filename] += "\n\n" + text
            else:
                chunks_by_source[filename] = text

     
        answer = generate_summary(
            chunks_by_source,
            query
        )

        sources = [
            {
                "filename": result["chunk"]["filename"],
                "score": result["score"]
            }
            for result in results
        ]

        return {
            "answer": answer,
            "sources": sources
        }
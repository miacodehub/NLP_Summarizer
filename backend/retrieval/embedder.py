from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str]):
    return model.encode(
        texts,
        normalize_embeddings=True
    )


def embed_query(query: str):
    return model.encode(
        [query],
        normalize_embeddings=True
    )
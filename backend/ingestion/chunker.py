def chunk_text(
    text: str,
    filename: str,
    chunk_size: int = 2000,
    overlap: int = 200
) -> list[dict]:

    if not text.strip():
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "text": chunk,
                "filename": filename
            })

        start += chunk_size - overlap

    return chunks
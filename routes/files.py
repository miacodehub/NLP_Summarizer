from fastapi import APIRouter, UploadFile, Form, HTTPException
from typing import List
from summarization.summarizer import generate_summary
from summarization.retriever import chunk_text, build_index, retrieve_relevant_chunks

router = APIRouter()

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

@router.post("/upload")
async def upload_files(
    files: List[UploadFile],
    keyword: str = Form(...)
):
    all_chunks = []

    for file in files:
        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"{file.filename} exceeds the 1MB limit")

        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a valid text file")

        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    if not all_chunks:
        raise HTTPException(status_code=400, detail="No content found in uploaded files.")

    index, _ = build_index(all_chunks)
    relevant_chunks = retrieve_relevant_chunks(keyword, all_chunks, index)

    if not relevant_chunks:
        return {"summary": f"No relevant content found for '{keyword}'.", "entries": []}

    combined = "\n".join(relevant_chunks)
    summary = generate_summary(combined)

    return {"summary": summary, "entries": relevant_chunks}
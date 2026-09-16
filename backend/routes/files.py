from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from ingestion.loader import extract_text
from ingestion.chunker import chunk_text
from retrieval.rag import RAGPipeline


router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/upload")
async def receive_files(
    files: list[UploadFile] = File(...),
    query: str = Form(...)
):
    all_chunks = []

    for file in files:
        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} exceeds the 5MB file size limit"
            )

        try:
            text = extract_text(
                file.filename,
                content
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not process {file.filename}: {str(e)}"
            )

        if not text.strip():
            continue

        chunks = chunk_text(
            text,
            file.filename
        )

        all_chunks.extend(chunks)

    if not all_chunks:
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the uploaded files."
        )

    rag = RAGPipeline(all_chunks)

    result = rag.answer(query)

    return result
from fastapi import APIRouter, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import List
from summarization.summarizer import generate_summary

router = APIRouter()

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB per file

class FileRequest(BaseModel):
    file_paths: list[str]


@router.post("/upload")
async def receive_files(
    files: List[UploadFile],
    keyword: str = Form(...)
):
    entries = []
    combined_context = ""

    for file in files:
        content = await file.read()

        # fix 1 - file size limit
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} exceeds the 1MB file size limit"
            )

        # fix 2 - non-utf-8 files
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a valid text file"
            )

        position = text.find(keyword)

        if position != -1:
            start = max(0, position - 100)
            end = min(len(text), position + 100)
            context = text[start:end]
            combined_context += context + "\n"
            entries.append({
                "filename": file.filename,
                "context": context
            })

    # fix 3 - empty context case
    if not combined_context.strip():
        return {
            "summary": f"No content found matching '{keyword}' in the uploaded files.",
            "entries": []
        }

    final_summary = generate_summary(combined_context)

    return {
        "summary": final_summary,
        "entries": entries
    }
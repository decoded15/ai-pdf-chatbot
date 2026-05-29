from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("data/uploads", exist_ok=True)

    file_path = f"data/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    chunks = chunk_text(extracted_text)

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "text_length": len(extracted_text),
        "total_chunks": len(chunks),
        "sample_chunk": chunks[0]
    }
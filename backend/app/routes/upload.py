from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("data/uploads", exist_ok=True)

    file_path = f"data/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename
    }
import os

from fastapi import APIRouter, UploadFile

from app.rag.loader import load_pdf, load_txt, load_docx
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding
from app.rag.vector_store import add_chunks

router = APIRouter()

UPLOAD_DIR = "data/documents"


@router.post("/upload")
async def upload(file: UploadFile):

    path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    # Detect file type
    if file.filename.lower().endswith(".pdf"):

        text = load_pdf(path)

    elif file.filename.lower().endswith(".txt"):

        text = load_txt(path)

    elif file.filename.lower().endswith(".docx"):
        text = load_docx(path)

    else:

        return {
            "status": "error",
            "message": "Only PDF, TXT and DOCX files are supported"
        }

    chunks = chunk_text(text)

    embeddings = [
        get_embedding(chunk)
        for chunk in chunks
    ]

    add_chunks(chunks, embeddings, file.filename)

    return {
        "status": "uploaded_and_indexed",
        "file": file.filename,
        "chunks": len(chunks)
    }
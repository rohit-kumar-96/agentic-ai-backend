import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.rag.loader import load_pdf, load_txt, load_docx
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding
from app.rag.vector_store import add_chunks

DOC_FOLDER = "data/documents"

for file in os.listdir(DOC_FOLDER):

    path = os.path.join(DOC_FOLDER, file)

    # Handle PDF
    if file.lower().endswith(".pdf"):

        if os.path.getsize(path) == 0:
            print(f"Skipping empty PDF: {file}")
            continue

        print(f"\nProcessing PDF: {file}")
        print(f"Size: {os.path.getsize(path)} bytes")

        text = load_pdf(path)

    # Handle TXT
    elif file.lower().endswith(".txt"):

        print(f"\nProcessing TXT: {file}")
        print(f"Size: {os.path.getsize(path)} bytes")

        text = load_txt(path)

    elif file.lower().endswith(".docx"):

        print(f"\nProcessing DOCX: {file}")

        text = load_docx(path)

    else:
        continue

    print(f"Text length: {len(text)}")

    chunks = chunk_text(text)

    print(f"Chunks created: {len(chunks)}")

    if len(chunks) == 0:
        print(f"No content found in {file}")
        continue

    try:

        embeddings = [
            get_embedding(chunk)
            for chunk in chunks
        ]

        add_chunks(chunks,embeddings,file)

        print(f"Indexed: {file}")

    except Exception as e:

        print(f"Failed indexing {file}")
        print(f"Error: {str(e)}")
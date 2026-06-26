from app.rag.retriever import retrieve


def retrieve_docs(query):
    return retrieve(query)
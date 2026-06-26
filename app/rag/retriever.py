# from app.rag.embeddings import get_embedding
# from app.rag.vector_store import search_chunks

# SIMILARITY_THRESHOLD = 1.5


# def retrieve(query):

#     query_embedding = get_embedding(query)

#     results = search_chunks(
#         query_embedding,
#         top_k=3
#     )

#     documents = results["documents"]
#     metadatas = results["metadatas"]
#     distances = results["distances"]

#     context_parts = []

#     for doc, meta, distance in zip(
#         documents,
#         metadatas,
#         distances
#     ):
        
#         print("DISTANCE:", distance)

#         if distance > SIMILARITY_THRESHOLD:
#             continue

#         source = meta.get(
#             "source",
#             "unknown"
#         )

#         context_parts.append(
#             f"""
# Source: {source}

# {doc}
# """
#         )

#     return "\n\n".join(
#         context_parts
#     )



from app.rag.embeddings import get_embedding
from app.rag.vector_store import search_chunks


def retrieve(query):

    query_embedding = get_embedding(query)

    results = search_chunks(
        query_embedding,
        top_k=3
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    context_parts = []

    for doc, meta in zip(
        documents,
        metadatas
    ):

        source = meta.get(
            "source",
            "unknown"
        )

        context_parts.append(
            f"""
Source: {source}

{doc}
"""
        )

    return "\n\n".join(
        context_parts
    )
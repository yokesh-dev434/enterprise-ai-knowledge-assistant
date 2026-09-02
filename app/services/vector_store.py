from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from .embedding_service import generate_embeddings
# from embedding_service import generate_embeddings
from .llm_service import generate_answer




# ---------------------------------------
# 1. Qdrant connection
# ---------------------------------------

client = QdrantClient(
    host="localhost",
    port=6333
)

collection_name = "knowledge_v1"


# ---------------------------------------
# 8. Similarity search
# ---------------------------------------

# def search_similar(query_vector, top_k=3):

#     results = client.query_points(
#         collection_name=collection_name,    
#         query=query_vector.tolist(),
#         limit=top_k
#     )

#     return results.points

def search_similar(query_vector,department, top_k=3):
    department_filter = Filter(
        must=[
            FieldCondition(
                key="department",
                match = MatchValue(value=department.title())
            )
        ]
    )
    results = client.query_points(
        collection_name=collection_name,
        query = query_vector.tolist(),
        query_filter=department_filter,
        limit=top_k
    )
    return results.points
     
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
# ---------------------------------------
# Qdrant connection
# ---------------------------------------

client = QdrantClient(
    host="localhost",
    port=6333
)
collection_name = "knowledge_v1"


# ---------------------------------------
# Similarity Search
# ---------------------------------------

def search_similar(
    query_vector,
    department,
    top_k=3
):

    department_filter = Filter(
        must=[
            FieldCondition(
                key="department",
                match=MatchValue(
                    value=department.title()
                )
            )
        ]
    )

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector.tolist(),
        query_filter=department_filter,
        limit=top_k
    )

    return results.points
from app.ingestion.ingest_document import client, collection_name
from qdrant_client.models import VectorParams, Distance
def reset_collection():

    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
        print("Old collection deleted.")

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("New collection created.")

if __name__ == "__main__":
    reset_collection()
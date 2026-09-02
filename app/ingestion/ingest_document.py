import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance,PointStruct

from ..services.document_processor import (
    extract_text,
    clean_text,
    chunk_text
)

from ..services.embedding_service import generate_embeddings

client = QdrantClient(
    host = "localhost",
    port = 6333
)


collection_name = "knowledge_v1"
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
    ))



def ingest_document(file_path, metadata):

    # extract
    raw_text = extract_text(file_path)

    # clean
    cleaned_text = clean_text(raw_text)

    # chunk
    
    chunks = chunk_text(cleaned_text)

    print("Number of chunks:", len(chunks))
    # embed
    embeddings = generate_embeddings(chunks)

    print("Number of embeddings:", len(embeddings))
    print("Embedding dimension:", len(embeddings[0]))
    # store in Qdrant

    points = []

    for chunk_index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload={
                "text": chunk,
                "document_id": metadata["document_id"],
                "chunk_index": chunk_index,
                "department": metadata["department"],
                "source": metadata["source"],
                "file_type": metadata["file_type"],
                "page": chunk_index + 1
            }
        )

        points.append(point)
    client.upsert(
        collection_name=collection_name,
        points=points
    )

    print("Inserted points:", len(points))
    
##########

# ---------------------------------------
# 3. Document path
# ---------------------------------------

# # file_path = "..\\uploads\\IT_01_VPN_Guide_TechNova_Solutions.docx"
# file_path = "app\\uploads\\IT_01_VPN_Guide_TechNova_Solutions.docx"


# # ---------------------------------------
# # 4. Extract and clean
# # ---------------------------------------

# raw_text = extract_text(file_path)

# cleaned_text = clean_text(raw_text)


# # ---------------------------------------
# # 5. Chunk
# # ---------------------------------------

# chunks = chunk_text(cleaned_text)

# print("Number of chunks:", len(chunks))


# # ---------------------------------------
# # 6. Generate embeddings
# # ---------------------------------------

# embeddings = generate_embeddings(chunks)

# print("Number of embeddings:", len(embeddings))
# print("Embedding dimension:", len(embeddings[0]))


# # ---------------------------------------
# # 7. Create Qdrant points
# # ---------------------------------------

# points = []

# for i, (chunk, embedding) in enumerate(
#     zip(chunks, embeddings)
# ):

#     point = PointStruct(
#         id=i,
#         vector=embedding.tolist(),
#         payload={
#             "text": chunk,
#             "source": "VPN_Guide_TechNova_Solutions",
#             "page": i + 1
#         }
#     )

#     points.append(point)


# # ---------------------------------------
# # 8. Store in Qdrant
# # ---------------------------------------

# client.upsert(
#     collection_name=collection_name,
#     points=points
# )

# print("Inserted points:", len(points))
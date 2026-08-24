# from app.services.rag_service import answer_question


# # user_query ="How do employees connect to the VPN?"
# user_query = "What is the employee maternity leave policy?"
# answer =answer_question(user_query)
# print("Final Answer:\n")
# print(answer)



###########################
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import search_similar


question = "What steps are required for remote access to company systems?"

query_embedding = generate_embeddings([question])[0]

results = search_similar(
    query_embedding,
    top_k=5
)
print("-"*100)
for result in results:
    print(f"\nScore: {result.score}")
    print(f"Source: {result.payload.get('source')}")
    print(f"Chunk: {result.payload.get('text')}")

print("-"*100)
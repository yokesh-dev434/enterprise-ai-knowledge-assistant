from .embedding_service import generate_embeddings
from .vector_store import search_similar
from .llm_service import generate_answer
from app.services.classifier_service import classifier_agent


SIMILARITY_THRESHOLD = 0.35

def answer_question(user_query):
    # meta_data_type_filtering
    classifier_response = classifier_agent(user_query)
    department = classifier_response.classifier
    print("Classified department:", department)
    if department == "UNKNOWN":
        return "I couldn't identify a relevant department for your question."
    # 1. Convert user question into an embedding
    query_embedding = generate_embeddings(
        [user_query]
    )[0]

    # 2. Search Qdrant
    results = search_similar(
        query_embedding,
        department=department,
        top_k=3
    )
    # print("-"*100)
    # print(results)
    # print("-"*100)

    # 3. Prepare retrieved chunks
    retrieved_chunks = []

    for result in results:
        # print("score",result.score)
        if result.score < SIMILARITY_THRESHOLD:
            continue
        retrieved_chunks.append({
            
            "text": result.payload["text"],
            "source": result.payload["source"],
            "page": result.payload["page"]
        })
    #  this step Will reduce the LLM call
    if retrieved_chunks ==[]:
        return "I couldn't find enough relevant information in the available documents."

    # 4. Instructions for Gemini
    prompt = """
    You are an enterprise knowledge assistant.

    Answer the user's question using only the provided context.

    If the answer is not available in the context,
    say that you don't have enough information.

    Do not make up information.
    """

    # 5. Generate final answer
    answer = generate_answer(
        prompt,
        user_query,
        retrieved_chunks
    )

    return answer
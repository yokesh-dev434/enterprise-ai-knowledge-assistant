from .embedding_service import generate_embeddings
from .vector_store import search_similar
from .llm_service import (
    generate_answer,
    generate_conversational_response
)
from app.services.classifier_service import classifier_agent
from app.services.standalone_service import standalone_query


SIMILARITY_THRESHOLD = 0.25


def answer_question(user_query, conversation_history):

    # 1. Convert the user's question into a standalone question
    standalone_question = standalone_query(
        user_query,
        conversation_history
    )

    # 2. Classify the question
    classifier_response = classifier_agent(
        standalone_question
    )

    department = classifier_response.classifier

    # 3. Handle greetings and acknowledgements
    if department in [
        "ACKNOWLEDGEMENT",
        "GREETING"
    ]:

        answer = generate_conversational_response(
            standalone_question
        )

        return answer, []

    # 4. Handle unknown questions
    if department == "UNKNOWN":

        return (
            "I couldn't identify a relevant department for your question.",
            []
        )

    # 5. Generate query embedding
    query_embedding = generate_embeddings(
        [standalone_question]
    )[0]

    # 6. Search Qdrant
    results = search_similar(
        query_embedding,
        department=department,
        top_k=3
    )

    # 7. Filter results using similarity threshold
    retrieved_chunks = []

    for result in results:

        if result.score < SIMILARITY_THRESHOLD:
            continue

        retrieved_chunks.append({
            "text": result.payload["text"],
            "source": result.payload["source"],
            "page": result.payload["page"]
        })

    # 8. Handle no relevant documents
    if not retrieved_chunks:

        return (
            "I couldn't find enough relevant information "
            "in the available documents.",
            []
        )

    # 9. Prompt for final answer
    prompt = """
        You are an enterprise knowledge assistant.

        Answer the user's current question using the retrieved
        company documents as the source of truth.

        Conversation history is provided only to understand
        the context of the conversation.

        Strict rules:
        1. Use only information available in the retrieved context
           to answer the question.
        2. Do not make up, assume, or infer information that is not
           present in the retrieved context.
        3. If the answer is not available in the retrieved context,
           respond exactly:
           "I don't have enough information."
        4. Conversation history must not override or replace
           information from the retrieved company documents.
        5. Keep the answer concise and relevant.
    """.strip()

    # 10. Generate final answer
    answer = generate_answer(
        prompt,
        user_query,
        retrieved_chunks,
        conversation_history
    )

    return answer, retrieved_chunks
# from app.services.rag_service import answer_question


# # user_query ="How do employees connect to the VPN?"
# user_query = "What is the employee maternity leave policy?"
# answer =answer_question(user_query)
# print("Final Answer:\n")
# print(answer)



###########################
from app.services.embedding_service import generate_embeddings
# from app.services.vector_store import search_similar


# question = "What steps are required for remote access to company systems?"

# query_embedding = generate_embeddings([question])[0]

# results = search_similar(
#     query_embedding,
#     top_k=5
# )
# print("-"*100)
# for result in results:
#     print(f"\nScore: {result.score}")
#     print(f"Source: {result.payload.get('source')}")
#     print(f"Chunk: {result.payload.get('text')}")

# print("-"*100)


from app.services.rag_service import answer_question


# HR
# question = "tell me the Working Hours of the company?"
# IT
# question ="how do i connect to the company VPN?"
# finance
# question = "How do i claim the expensive?"
# project
# question = "Who owns Project Alpha?"
# engineer
question = "What is the standard procedure for creating and merging code changes?"

# question = "What should I do before accessing internal company systems remotely?"
# question = "How do I reset my company email password?"
# question = "What is the weather in Vellore today?"
# question ="how do i install the microsoft in my company laptop?"
# question = "what is the caffiteria menu?"

print("-"*100)
# question ="How do I submit an expense claim?"

# question = "What should an employee do to get reimbursed for a business expense?"
# finance
# question = "What is the maximum amount I can claim for a business expense?"
# unknown
# question = "What is the weather in Vellore today?"

############## 
# engineer 
# question = "What is the standard process for merging a feature branch?"
# question = "I have finished developing a new feature. What should I do before my code is merged into the development branch?"
# question ="What is the maximum number of commits allowed in a feature branch?"
# question ="How do I submit a travel expense claim?"
# question = "What should I do after creating a new feature branch before it can be merged?"
# question ="How do I submit a travel expense claim?"

answer = answer_question(question)

print(answer)
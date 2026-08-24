import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(prompt,user_query,retrived_chunks):
    context = "\n\n".join(
        chunk["text"] for chunk in retrived_chunks
    )
    final_prompt = f"""
        {prompt}

        Context:
        {context}

        User Question:
        {user_query}
        """
    response =client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=final_prompt
    )      
    return response.text

# old_model ="gemini-3.6-flash"
# if __name__ == "__main__":

#     answer = generate_answer(
#         "Explain what RAG is in two sentences."
#     )

#     print(answer)
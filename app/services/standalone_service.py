import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def standalone_query(user_query, conversational_history):

    query_rewrite_prompt = f"""
You are a query rewriting assistant.

Your task is to make the user's question standalone using the conversation history.

Rules:
1. If the user query is already clear and standalone, return it unchanged.
2. If the query depends on previous conversation, rewrite it using the necessary context from the conversation history.
3. Do not change the user's actual meaning.
4. Do not add new information.
5. Return only the final standalone query. No explanation.

Conversation History:
{conversational_history}

User Query:
{user_query}
""".strip()

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=query_rewrite_prompt,
            config=types.GenerateContentConfig(
                temperature=0.3
            )
        )

    except errors.ServerError as e:

        print("Primary model failed:", e)
        print("Trying fallback model...")

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=query_rewrite_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3
                )
            )

        except errors.ServerError as e:

            print("Fallback model also failed:", e)

            # If rewriting fails, use the original question
            return user_query

    return response.text
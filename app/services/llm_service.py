import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(
    prompt,
    user_query,
    retrieved_chunks,
    conversation_history
):

    history = "\n\n".join(
        f"User: {json.loads(turn)['user']}\n"
        f"Assistant: {json.loads(turn)['assistant']}"
        for turn in conversation_history
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    final_prompt = f"""
        {prompt}

        Conversation History:
        {history}

        Context:
        {context}

        User Question:
        {user_query}
    """

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=final_prompt,
            config=types.GenerateContentConfig(
                temperature=0.1
            )
        )

    except Exception as e:

        print("Primary model failed:", e)
        print("Trying fallback model...")

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=final_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )

        except Exception as e:

            print("Fallback model also failed:", e)

            return (
                "The AI service is temporarily unavailable. "
                "Please try again in a moment."
            )

    return response.text


def generate_conversational_response(user_query):

    prompt = f"""
        You are a helpful enterprise AI assistant.

        The user has sent a greeting or acknowledgement.

        Respond naturally and briefly.

        Do not use company documents.
        Do not invent company-specific information.

        User message:
        {user_query}
    """

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3
            )
        )

    except Exception as e:

        print("Primary model failed:", e)
        print("Trying fallback model...")

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3
                )
            )

        except Exception as e:

            print("Fallback model also failed:", e)

            return (
                "The AI service is temporarily unavailable. "
                "Please try again in a moment."
            )

    return response.text
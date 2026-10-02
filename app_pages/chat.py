import json

import requests
import streamlit as st


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = None


# ---------------- AUTH ----------------

token = st.session_state["access_token"]


# ---------------- SIDEBAR ----------------

if st.sidebar.button("🚪 Logout"):

    st.session_state["logged_in"] = False
    st.session_state["access_token"] = None
    st.session_state["messages"] = []
    st.session_state["session_id"] = None

    st.rerun()


if st.sidebar.button("➕ New Chat"):

    st.session_state["messages"] = []
    st.session_state["session_id"] = None

    st.rerun()


st.sidebar.subheader("Recent Chats")


# ---------------- RECENT CHATS ----------------

try:

    response = requests.get(
        "http://127.0.0.1:8000/chat/sessions",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=10
    )

    if response.status_code == 200:

        chat_sessions = response.json()

        for session_id, first_message in chat_sessions.items():

            if st.sidebar.button(
                first_message,
                key=f"chat_{session_id}"
            ):

                st.session_state["session_id"] = session_id

                conversation_response = requests.get(
                    f"http://127.0.0.1:8000/chat/sessions/{session_id}",
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    timeout=10
                )

                if conversation_response.status_code == 200:

                    conversation_data = conversation_response.json()

                    conversation = conversation_data["conversation"]

                    st.session_state["messages"] = []

                    for turn in conversation:

                        turn_data = json.loads(turn)

                        st.session_state["messages"].append({
                            "role": "user",
                            "content": turn_data["user"]
                        })

                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": turn_data["assistant"]
                        })

                    st.rerun()

                else:

                    st.error(
                        "Unable to load this conversation."
                    )

    else:

        st.error("Unable to load recent chats.")

except requests.RequestException:

    st.error(
        "Unable to connect to the backend. "
        "Please make sure the FastAPI server is running."
    )


# ---------------- CHAT TITLE ----------------

st.title("Enterprise AI Knowledge Assistant")


# ---------------- DISPLAY MESSAGES ----------------

for message in st.session_state["messages"]:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                with st.expander("📚 Sources"):

                    for source in sources:

                        st.write(f"• {source}")


# ---------------- CHAT INPUT ----------------

user_query = st.chat_input("Ask your question")


if user_query:

    st.session_state["messages"].append({
        "role": "user",
        "content": user_query
    })

    with st.spinner("Loading..."):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/chat/main_chat",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                json={
                    "user_query": user_query,
                    "session_id": st.session_state["session_id"]
                },
                timeout=30
            )

        except requests.RequestException:

            st.error(
                "Unable to connect to the backend. "
                "Please make sure the FastAPI server is running."
            )

            st.stop()


    # ---------------- API RESPONSE ----------------

    if response.status_code != 200:

        st.error(
            f"API Error: {response.status_code}"
        )

        st.write(response.text)

        st.stop()


    response_data = response.json()

    st.session_state["session_id"] = response_data["session_id"]

    assistant_response = response_data["final_answer"]
    sources = response_data["sources"]


    # ---------------- STORE ASSISTANT RESPONSE ----------------

    st.session_state["messages"].append({
        "role": "assistant",
        "content": assistant_response,
        "sources": sources
    })

    st.rerun()
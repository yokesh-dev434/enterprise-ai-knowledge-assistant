import requests
import streamlit as st


# ---------------- LOGIN PAGE ----------------

def login_page():

    st.title("Enterprise AI Knowledge Assistant")
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    login_button = st.button("Login")

    if login_button:

        if not username or not password:
            st.error("Username and password are required")
            return

        with st.spinner("Loading..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/login/LoginCredential",
                    json={
                        "user_name": username,
                        "password": password
                    },
                    timeout=10
                )

                if response.status_code == 200:

                    token = response.json()["access_token"]

                    st.session_state["access_token"] = token
                    st.session_state["logged_in"] = True

                    st.rerun()

                else:
                    st.error("Invalid username or password")

            except requests.RequestException:
                st.error(
                    "Unable to connect to the backend. "
                    "Please make sure the FastAPI server is running."
                )


# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# ---------------- PAGES ----------------

login = st.Page(
    login_page,
    title="Login"
)

chat = st.Page(
    "app_pages/chat.py",
    title="Chat"
)

document_upload = st.Page(
    "app_pages/document_upload.py",
    title="Document Upload"
)


# ---------------- NAVIGATION ----------------

if st.session_state["logged_in"]:

    pg = st.navigation(
        [chat, document_upload],
        position="sidebar"
    )

else:

    pg = st.navigation(
        [login],
        position="hidden"
    )


# ---------------- RUN ----------------

pg.run()
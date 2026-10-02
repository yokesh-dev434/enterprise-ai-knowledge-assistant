import requests
import streamlit as st


# ---------------- AUTH ----------------

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()


# ---------------- PAGE ----------------

st.title("📄 Document Upload")

st.write("Upload a company document to the knowledge base.")


# ---------------- FILE ----------------

uploaded_file = st.file_uploader(
    "Select Document",
    type=["pdf", "docx", "txt"]
)


# ---------------- DEPARTMENT ----------------

department = st.selectbox(
    "Select Department",
    [
        "HR",
        "IT",
        "Client",
        "Engineering",
        "PROJECTS",
        "Finance"
    ]
)


# ---------------- UPLOAD ----------------

if st.button("Upload Document"):

    if uploaded_file is None:
        st.warning("Please select a document.")
        st.stop()

    token = st.session_state["access_token"]

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    data = {
        "department": department
    }

    with st.spinner("Uploading and processing document..."):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/documents/",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                files=files,
                data=data,
                timeout=60
            )

        except requests.RequestException:

            st.error(
                "Unable to connect to the backend. "
                "Please make sure the FastAPI server is running."
            )

            st.stop()


    if response.status_code == 200:

        st.success(
            "Document uploaded and processed successfully!"
        )

    else:

        st.error(
            f"Upload failed: {response.status_code}"
        )
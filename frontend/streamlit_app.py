import streamlit as st
import requests


st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide"
)


st.title("AI PDF Chatbot")
st.caption("Chat with your PDF using RAG + Gemini")


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf"
    )

    if uploaded_file:

        with st.spinner("Processing PDF..."):

            files = {
                "file": uploaded_file
            }

            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files
            )

            result = response.json()

        st.success("PDF processed successfully!")

        st.write("Chunks Created:",
                 result["total_chunks"])

        st.write(
            "Embedding Dimension:",
            result["embedding_dimension"]
        )


# ---------------- CHAT HISTORY ---------------- #

if "messages" not in st.session_state:

    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------- CHAT INPUT ---------------- #

query = st.chat_input(
    "Ask a question about your PDF..."
)


if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = requests.get(
                "http://127.0.0.1:8000/chat",
                params={"query": query}
            )

            result = response.json()

            answer = result["response"]

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
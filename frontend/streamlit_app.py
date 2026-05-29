import time
import streamlit as st
import requests


st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide"
)


# ---------------- HEADER ---------------- #

st.title("📄 AI PDF Chatbot")
st.caption(
    "Chat with your PDF using RAG + Gemini"
)


# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("📂 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type="pdf"
    )

    if uploaded_file:

        with st.status(
            "Processing PDF...",
            expanded=True
        ) as status:

            st.write("Saving PDF...")

            files = {
                "file": uploaded_file
            }

            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files
            )

            result = response.json()

            st.write("Extracting text...")
            time.sleep(0.5)

            st.write("Chunking document...")
            time.sleep(0.5)

            st.write("Generating embeddings...")
            time.sleep(0.5)

            st.write("Creating vector index...")
            time.sleep(0.5)

            status.update(
                label="✅ PDF Ready!",
                state="complete"
            )

        st.session_state.pdf_uploaded = True

        st.success("Document indexed successfully!")

        st.info(
            f"""
            📑 Chunks: {result["total_chunks"]}

            🧠 Embedding Dimension:
            {result["embedding_dimension"]}
            """
        )


# ---------------- CHAT HISTORY ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------- CHAT INPUT ---------------- #

if st.session_state.pdf_uploaded:

    query = st.chat_input(
        "Ask a question about your PDF..."
    )

else:

    query = None

    st.warning(
        "Upload a PDF to start chatting."
    )


# ---------------- USER QUERY ---------------- #

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    # ---------------- AI RESPONSE ---------------- #

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        with st.spinner("Thinking..."):

            response = requests.get(
                "http://127.0.0.1:8000/chat",
                params={"query": query}
            )

            result = response.json()

            answer = result["response"]

            # Simulated streaming effect

            full_response = ""

            for word in answer.split():

                full_response += word + " "

                time.sleep(0.03)

                response_placeholder.markdown(
                    full_response + "▌"
                )

            response_placeholder.markdown(
                full_response
            )

        # ---------------- SOURCES ---------------- #

        with st.expander("📚 Retrieved Sources"):

            for i, chunk in enumerate(
                result["retrieved_chunks"]
            ):

                st.markdown(
                    f"### Chunk {i+1}"
                )

                st.write(chunk)

                st.divider()

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
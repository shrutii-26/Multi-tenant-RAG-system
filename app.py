import streamlit as st
import uuid
import os
import tempfile

from ingestion import build_index_for_upload
from retrieval import retrieve
from generator import generate_answer

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Tenant RAG System",
    page_icon="🧠",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
}

/* Background */
.stApp {
    background: #0f0f0f;
    color: #f0ede6;
}

/* Cards */
.rag-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}

/* Answer box */
.answer-box {
    background: #141414;
    border-left: 3px solid #c9a84c;
    border-radius: 0 10px 10px 0;
    padding: 20px 24px;
    line-height: 1.8;
    color: #f0ede6;
    font-size: 15px;
    margin-top: 12px;
}

/* Source pill */
.source-pill {
    display: inline-block;
    background: #222;
    border: 1px solid #333;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    color: #999;
    margin: 4px 4px 0 0;
}

/* KB badge */
.kb-badge {
    background: #1e1e1e;
    border: 1px solid #c9a84c44;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 12px;
    color: #c9a84c;
    word-break: break-all;
    margin-top: 12px;
}

/* Streamlit button override */
.stButton > button {
    background: #c9a84c !important;
    color: #0f0f0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #1a1a1a;
    border: 1px dashed #333;
    border-radius: 10px;
    padding: 10px;
}

/* Text area */
textarea {
    background: #1a1a1a !important;
    color: #f0ede6 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
}

/* Divider */
hr {
    border-color: #222 !important;
}

/* Success / error */
.stAlert {
    border-radius: 8px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "kb_id" not in st.session_state:
    st.session_state.kb_id = None
if "answer" not in st.session_state:
    st.session_state.answer = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🧠 Multi-Tenant RAG System")
st.markdown(
    "<p style='color:#888; margin-top:-10px; margin-bottom:28px;'>"
    "Upload your documents and query them using Retrieval-Augmented Generation."
    "</p>",
    unsafe_allow_html=True,
)

st.divider()

# ── Upload section ────────────────────────────────────────────────────────────
st.markdown("### 📂 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

if st.button("Build Knowledge Base", disabled=not uploaded_files):
    with st.spinner("Processing your documents..."):
        try:
            kb_id = str(uuid.uuid4())
            tmp_dir = tempfile.mkdtemp()

            for uploaded_file in uploaded_files:
                file_path = os.path.join(tmp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())

            build_index_for_upload(tmp_dir, kb_id)
            st.session_state.kb_id = kb_id
            st.session_state.answer = None
            st.success("Knowledge base built successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.kb_id:
    st.markdown(
        f"<div class='kb-badge'>🗂 Knowledge Base ID: {st.session_state.kb_id}</div>",
        unsafe_allow_html=True,
    )

st.divider()

# ── Query section ─────────────────────────────────────────────────────────────
st.markdown("### 💬 Ask a Question")

question = st.text_area(
    "Your question",
    placeholder="What does the document say about...?",
    height=120,
    label_visibility="collapsed",
)

if st.button("Get Answer", disabled=not (st.session_state.kb_id and question.strip())):
    with st.spinner("Thinking..."):
        try:
            context, _, diagnostics = retrieve(
                query=question,
                kb_name=st.session_state.kb_id,
            )
            answer = generate_answer(context, question)
            st.session_state.answer = answer
        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.answer:
    st.divider()
    st.markdown("### 📝 Answer")
    st.markdown(
        f"<div class='answer-box'>{st.session_state.answer}</div>",
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<p style='text-align:center; color:#444; font-size:12px; margin-top:48px;'>"
    "Built with FastAPI · FAISS · Groq LLM · Streamlit"
    "</p>",
    unsafe_allow_html=True,
)

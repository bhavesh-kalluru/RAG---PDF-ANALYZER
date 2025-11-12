import os, streamlit as st
from dotenv import load_dotenv
from utils.pdf_utils import pdf_bytes_to_text
from utils.embedding import chat_complete_text
from scripts.index_builder import run as build_index
from scripts.retrieve import retrieve

load_dotenv()
st.set_page_config(page_title="RAG PDF Assistant", page_icon="📘")

st.title("📘 RAG Assistant (PDF Uploads)")
st.write("Upload PDFs or TXTs, rebuild the FAISS index, and ask grounded questions.")

with st.expander("📄 Upload PDF or TXT files"):
    uploaded = st.file_uploader("Upload files", type=["pdf", "txt"], accept_multiple_files=True)
    if uploaded:
        os.makedirs("data", exist_ok=True)
        for f in uploaded:
            if f.name.lower().endswith(".pdf"):
                txt = pdf_bytes_to_text(f.read())
                open(f"data/{os.path.splitext(f.name)[0]}.txt", "w").write(txt)
            else:
                open(f"data/{f.name}", "wb").write(f.read())
        st.success("Files saved to ./data")

if st.button("🔨 Rebuild Index"):
    try:
        build_index()
        st.success("Index rebuilt successfully!")
    except Exception as e:
        st.error(str(e))

st.divider()
query = st.text_input("Your question")
topk = st.slider("Top-K Contexts", 2, 8, 4)

if st.button("Ask"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Please set your OPENAI_API_KEY in .env")
    elif not os.path.exists("index/chunks.index"):
        st.error("Please rebuild the index first.")
    else:
        ctxs = retrieve(query, k=topk)
        if not ctxs:
            st.warning("No results found.")
        else:
            st.write("### Retrieved Context")
            for i, c in enumerate(ctxs, 1):
                st.markdown(
                    f"**{i}.** _score={c['score']:.3f}_  \n**Source:** {c['meta']['source']} (chunk {c['meta']['chunk_id']})\n{c['text']}"
                )
            sys = {"role": "system", "content": "Answer only using the provided context."}
            context = "\n\n".join([f"[{i}] {c['text']}" for i, c in enumerate(ctxs)])
            usr = {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"}
            try:
                ans = chat_complete_text([sys, usr])
                st.success("Answer")
                st.write(ans)
            except Exception as e:
                st.error(str(e))

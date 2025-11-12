📘 Streamlit RAG PDF Assistant

Streamlit RAG PDF Assistant is an interactive application that lets users upload PDF or text documents, automatically extract and embed their contents, and then ask natural language questions about the uploaded material using Retrieval-Augmented Generation (RAG) powered by OpenAI.

This app combines document retrieval (via FAISS vector search) and AI-based question answering (via GPT-4o / GPT models) to provide contextually accurate, grounded responses directly from your uploaded documents.

🚀 Features

✅ PDF and TXT Uploads
Upload multiple PDF or text files. The app automatically extracts text from PDFs (no OCR required) and stores it in the data/ folder.

✅ Automatic Text Chunking & Embedding
Each document is split into overlapping text chunks, converted into embeddings using OpenAI’s text-embedding-3-small model, and indexed locally with FAISS for fast similarity search.

✅ Retrieval-Augmented Question Answering (RAG)
When you enter a question, the app retrieves the most relevant chunks from your uploaded files and uses GPT-4o to generate an answer grounded in those retrieved passages.

✅ Built with Streamlit
Runs locally or on Streamlit Cloud with an intuitive interface — no command-line skills required.

✅ Supports OpenAI SDK v2.x and v1.x
Fully compatible with modern OpenAI SDKs, using fallback logic for older environments.

🧩 Tech Stack

Frontend: Streamlit

Backend / Embeddings: OpenAI API (GPT-4o, text-embedding-3-small)

Vector Database: FAISS (in-memory cosine similarity search)

Document Handling: PyPDF

Environment Management: python-dotenv

🛠️ How It Works

Upload documents → PDFs are automatically converted to text.

Build the FAISS index → Text chunks are embedded and stored locally.

Ask a question → Retrieves top relevant passages using similarity search.

Generate an answer → GPT uses the retrieved context to provide a grounded response.

⚙️ Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Add your OpenAI API key
streamlit run app.py

📂 Folder Structure
streamlit_rag_pdf_app_final/
├── app.py
├── requirements.txt
├── .env.example
├── utils/
│   ├── embedding.py
│   └── pdf_utils.py
├── scripts/
│   ├── index_builder.py
│   └── retrieve.py
└── data/

💡 Example Use Cases

HR or Policy Assistants — Upload company handbooks and query HR policies.

Legal or Research Summaries — Quickly answer questions from contracts or reports.

Academic Notes — Upload papers or class notes to generate summaries or insights.

Knowledge Base Chatbots — Build your own internal Q&A system with local docs.

Multi-Tenant Retrieval-Augmented Generation (RAG) System

A full-stack AI system that allows users to upload their own PDF documents and query them using Retrieval-Augmented Generation (RAG).

Each upload creates an isolated knowledge base with dynamic FAISS indexing, enabling per-user document querying.

.

🚀 Features

Dynamic PDF upload

Automatic text extraction and chunking

Per-upload FAISS vector index creation

Retrieval-based context grounding

LLM-based answer generation (Groq)

Source citation display

Knowledge base isolation using unique IDs

Full-stack deployment (FastAPI + React)

🏗 Architecture
Backend

FastAPI – REST API layer

FAISS – Vector similarity search

SentenceTransformers (all-MiniLM-L6-v2) – Embeddings

Groq LLM API – Answer generation

PyPDF2 – PDF text extraction

Frontend

React (Vite) – UI layer

REST API integration

Dynamic upload and query interface

🔄 System Flow

User uploads one or more PDF documents.

Backend extracts text using PyPDF2.

Text is split into overlapping chunks.

Embeddings are generated using SentenceTransformers.

A FAISS index is built and stored per unique knowledge base ID.

User submits a question.

Top-k relevant chunks are retrieved from FAISS.

Retrieved context is sent to the LLM.

Grounded answer + sources are returned to the frontend.

📂 Project Structure
comparative-rag-project/
│
├── backend/
│ ├── main.py
│ ├── ingestion.py
│ ├── retrieval.py
│ ├── generator.py
│ └── config.py
│
├── frontend/
│ └── src/App.jsx
│
├── indexes/ # auto-generated (ignored in git)
├── .env # environment variables (ignored in git)
└── README.md

🔐 Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

🛠 Local Development
1️⃣ Backend
uvicorn backend.main:app --reload

Runs at:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs

2️⃣ Frontend
cd frontend
npm install
npm run dev

Runs at:

http://localhost:5173

🌐 Deployment

Backend

Deploy to Render

Start command:

uvicorn backend.main:app --host 0.0.0.0 --port 10000

Frontend

Deploy frontend/ directory to Vercel

Update API URLs to deployed backend URL

📌 Why This Project Matters

This project demonstrates:

Multi-tenant AI system design

Retrieval-Augmented Generation (RAG)

Vector search implementation using FAISS

Dynamic knowledge base isolation

Production-ready REST API architecture

Full-stack AI deployment

Error handling and clean API responses

⚙️ Future Improvements

User authentication layer

Persistent cloud storage (S3 / database)

Streaming LLM responses

Better UI/UX design

Rate limiting and usage controls

👩‍💻 Author

Built as a production-style AI engineering project demonstrating full-stack RAG deployment.

# Deploy backend on Render

Quick steps to deploy the `backend` on Render.

1. Connect your repository to Render (GitHub/GitLab).
2. Let Render detect `render.yaml` in repository root — it will create a web service named `comparative-rag-backend`.
   - The `render.yaml` runs `pip install -r backend/requirements.txt` and starts the app with:
     `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add required environment variables in the Render dashboard (example):
   - `GROQ_API_KEY` — your Groq API key
   - Any other secrets your app needs
4. Render provides the `PORT` env var automatically; no change needed for it.
5. Local testing:

```
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. After deploy, check service logs and hit `/` to confirm `{"status":"RAG API running"}`.

Notes:

- Running `uvicorn` from within `backend` ensures local imports like `ingestion` and `retrieval` work without package changes.
- If you prefer gunicorn, add it to `backend/requirements.txt` and change the start command accordingly.

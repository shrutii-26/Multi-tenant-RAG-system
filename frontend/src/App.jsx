import { useState } from "react";

function App() {
  const [files, setFiles] = useState(null);
  const [kbId, setKbId] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const uploadFiles = async () => {
    if (!files) {
      setError("Please select PDF files first.");
      return;
    }

    setError("");
    setLoading(true);

    const formData = new FormData();
    for (let file of files) {
      formData.append("files", file);
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setKbId(data.kb_id);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  const askQuestion = async () => {
    if (!kbId) {
      setError("Upload documents before asking questions.");
      return;
    }

    if (!question) {
      setError("Enter a question.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: question,
          kb_name: kbId,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Query failed");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Multi-Tenant RAG System</h1>
      <p style={styles.subtitle}>
        Upload your documents and query them using Retrieval-Augmented Generation.
      </p>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.card}>
        <h2>Upload Documents</h2>
        <input
          type="file"
          multiple
          onChange={(e) => setFiles(e.target.files)}
        />
        <button style={styles.button} onClick={uploadFiles}>
          Upload
        </button>

        {kbId && (
          <div style={styles.kbBox}>
            <strong>Knowledge Base ID:</strong>
            <div style={styles.kbId}>{kbId}</div>
          </div>
        )}
      </div>

      <div style={styles.card}>
        <h2>Ask a Question</h2>
        <textarea
          rows="4"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={styles.textarea}
          placeholder="Enter your question..."
        />
        <button style={styles.button} onClick={askQuestion}>
          Ask
        </button>
      </div>

      {loading && <p style={styles.loading}>Processing...</p>}

      {answer && (
        <div style={styles.card}>
          <h2>Answer</h2>
          <div style={styles.answer}>{answer}</div>
        </div>
      )}

      {sources.length > 0 && (
        <div style={styles.card}>
          <h2>Sources</h2>
          <ul>
            {sources.map((src, index) => (
              <li key={index}>{src}</li>
            ))}
          </ul>
        </div>
      )}

      <footer style={styles.footer}>
        Built with FastAPI, FAISS, and Groq LLM
      </footer>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "900px",
    margin: "60px auto",
    padding: "0 20px",
    fontFamily: "Inter, sans-serif",
    color: "#1a1a1a",
  },
  title: {
    textAlign: "center",
    fontSize: "30px",
    fontWeight: "600",
  },
  subtitle: {
    textAlign: "center",
    marginBottom: "40px",
    color: "#555",
  },
  card: {
    background: "#fff",
    padding: "28px",
    borderRadius: "14px",
    boxShadow: "0 6px 20px rgba(0,0,0,0.06)",
    marginBottom: "28px",
  },
  textarea: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    marginBottom: "12px",
  },
  button: {
    padding: "10px 18px",
    borderRadius: "8px",
    border: "none",
    background: "#111",
    color: "#fff",
    cursor: "pointer",
    marginTop: "10px",
  },
  loading: {
    textAlign: "center",
    fontWeight: "500",
  },
  answer: {
    whiteSpace: "pre-wrap",
    lineHeight: "1.6",
  },
  kbBox: {
    marginTop: "15px",
    background: "#f4f4f4",
    padding: "12px",
    borderRadius: "8px",
  },
  kbId: {
    wordBreak: "break-all",
    fontSize: "13px",
    marginTop: "6px",
  },
  error: {
    background: "#ffe5e5",
    color: "#b00020",
    padding: "10px",
    borderRadius: "8px",
    marginBottom: "20px",
  },
  footer: {
    textAlign: "center",
    marginTop: "50px",
    fontSize: "13px",
    color: "#777",
  },
};

export default App;
import { useState } from "react";
import "./Titleform.css"

function TitleForm({ onResult }) {
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) return;

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8001/api/verify-title", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ title })
      });

      const data = await response.json();
      onResult(data);
    } catch (error) {
      console.error("API Error:", error);
      onResult({ error: "Backend not reachable" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="title-form" onSubmit={handleSubmit}>
      <label htmlFor="titleInput">Enter Title</label>

      <input
        id="titleInput"
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter title here"
      />

      <button type="submit" disabled={loading}>
        {loading ? "Verifying..." : "Verify Title"}
      </button>
    </form>
  );
}

export default TitleForm;
import { useState } from "react";
import "./ResultCard.css";

function TitleForm({ onResult }) {
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) return;

    setLoading(true);

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 30000); // ⏱ 30s timeout

      const response = await fetch("http://localhost:8000/api/verify-title", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title }),
        signal: controller.signal,
      });

      clearTimeout(timeout);

      // 🚨 Check if API failed
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      console.log("✅ API Response:", data); // 🔥 Debug

      onResult(data);

    } catch (error) {
      console.error("❌ API Error:", error);

      if (error.name === "AbortError") {
        onResult({ error: "Request timed out (server too slow)" });
      } else {
        onResult({ error: "Backend error or not reachable" });
      }

    } finally {
      setLoading(false); // ✅ ALWAYS stops loading
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
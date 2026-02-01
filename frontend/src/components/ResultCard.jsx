import "./ResultCard.css"

function ResultCard({ result }) {
  if (!result) return null;

  if (result.error) {
    return <p className="error-message">{result.error}</p>;
  }

  return (
    <div className="result-card">
      <h3>Verification Result</h3>

      <p><strong>Status:</strong> {result.status}</p>
      <p><strong>Verification Probability:</strong> {result.verification_probability}%</p>
      <p><strong>Similarity Percentage:</strong> {result.similarity_percentage}%</p>

      {result.closest_match && (
        <p><strong>Closest Match:</strong> {result.closest_match}</p>
      )}

      {result.rejection_reasons && result.rejection_reasons.length > 0 && (
        <>
          <strong>Reasons:</strong>
          <ul>
            {result.rejection_reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default ResultCard;
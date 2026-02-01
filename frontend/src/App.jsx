import { useState } from "react";
import "./styles/App.css";
import TitleForm from "./components/TitleForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app-container">
      <h1>PRGI Title Verification System</h1>
      <p>AI-based title verification</p>

      <TitleForm onResult={setResult} />
      <ResultCard result={result}/>

      
    </div>
  );
}

export default App;

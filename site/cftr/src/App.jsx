import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    residue_location: "",
    current_residue: "",
    mutated_residue: "",
    structure: "", // Not used but included for UI completeness
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/predict", {
        residue_location: formData.residue_location,
        current_residue: formData.current_residue,
        mutated_residue: formData.mutated_residue,
      });
      setResult(response.data.classification);
    } catch (error) {
      console.error("Error:", error);
      setResult("Error fetching prediction");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>CFTR Scanner</h1>
      <form onSubmit={handleSubmit} className="mutation-form">
        <input
          type="text"
          name="residue_location"
          value={formData.residue_location}
          onChange={handleChange}
          placeholder="Residue Location"
          required
        />
        <input
          type="text"
          name="current_residue"
          value={formData.current_residue}
          onChange={handleChange}
          placeholder="Current Residue"
          required
        />
        <input
          type="text"
          name="mutated_residue"
          value={formData.mutated_residue}
          onChange={handleChange}
          placeholder="Mutated Residue"
          required
        />
        <input
          type="text"
          name="structure"
          value={formData.structure}
          onChange={handleChange}
          placeholder="Structure (not used)"
        />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Run"}
        </button>
      </form>
      {result && <p className="result"><strong>Prediction:</strong> {result}</p>}
    </div>
  );
}

export default App;

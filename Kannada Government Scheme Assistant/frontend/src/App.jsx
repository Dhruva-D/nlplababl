import React, { useState } from 'react';
import './App.css';
import { searchScheme } from './services/api';

function App() {
  const [query, setQuery] = useState('');
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setScheme(null);

    try {
      const response = await searchScheme(query);
      if (response && response.result) {
        setScheme(response.result);
      } else {
        setError('No matching scheme found. Try rephrasing your search.');
      }
    } catch (err) {
      setError('Failed to connect to the backend server. Is FastAPI running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1 className="title">Kannada Scheme Assistant</h1>
        <p className="subtitle">AI-Powered Government Benefit Finder</p>
      </div>

      <form className="search-box" onSubmit={handleSearch}>
        <input 
          type="text" 
          className="kannada-input" 
          placeholder="What kind of assistance do you need? (e.g., ಮಹಿಳೆಯರಿಗೆ ಹಣಕಾಸು ಸಹಾಯ)" 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" className="search-btn" disabled={loading}>
          {loading ? <div className="spinner"></div> : "Search Schemes"}
        </button>
      </form>

      {error && (
        <div className="no-match">
          {error}
        </div>
      )}

      {scheme && (
        <div className="result-card">
          <h2 className="scheme-title">{scheme.scheme_name}</h2>
          <p className="scheme-desc">{scheme.description}</p>
          
          <div className="tags-container">
            {scheme.keywords && scheme.keywords.map((tag, idx) => (
              <span key={idx} className="tag">#{tag}</span>
            ))}
            {scheme.ai_confidence_score && (
              <span className="tag" style={{background: 'rgba(139, 92, 246, 0.1)', color: '#8b5cf6', borderColor: 'rgba(139, 92, 246, 0.2)'}}>
                AI Match: {(scheme.ai_confidence_score * 100).toFixed(1)}%
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

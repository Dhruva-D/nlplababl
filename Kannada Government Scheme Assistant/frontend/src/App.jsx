import React, { useState } from 'react';
import './App.css';
import { searchScheme } from './services/api';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const response = await searchScheme(query);
      if (response && response.results && response.results.length > 0) {
        setResults(response.results);
      } else {
        // Use the message from the backend if provided, else a fallback
        setError(response?.message || 'No relevant government scheme found.');
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

      {error && <div className="no-match">{error}</div>}

      {results.length > 0 && (
        <div className="results-list">
          <p className="results-header">Top {results.length} Matching Schemes</p>
          {results.map((scheme, idx) => (
            <div className="result-card" key={scheme._id || idx}>
              <div className="rank-badge">#{idx + 1}</div>
              <h2 className="scheme-title">{scheme.scheme_name}</h2>
              <p className="scheme-desc">{scheme.description}</p>
              <div className="tags-container">
                {scheme.keywords && scheme.keywords.map((tag, i) => (
                  <span key={i} className="tag">#{tag}</span>
                ))}
                <span className="tag confidence-tag">
                  AI Match: {scheme.ai_confidence_score}%
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;

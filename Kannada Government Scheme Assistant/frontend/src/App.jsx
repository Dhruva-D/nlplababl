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
      <div className="hero-section">
        <div className="hero-badge">
          <span className="badge-icon">✨</span>
          <span>Powered by Advanced NLP AI</span>
        </div>
        <h1 className="hero-title">
          Discover Your <span>Government Schemes</span> Instantly
        </h1>
        <p className="hero-subtitle">
          An intelligent assistant to find the perfect Karnataka & Central Government schemes for you. Just type what you need in English or Kannada.
        </p>

        <form className="hero-search-box" onSubmit={handleSearch}>
          <div className="input-group">
            <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input
              type="text"
              className="hero-input"
              placeholder="Try 'ಮಹಿಳೆಯರಿಗೆ ಹಣಕಾಸು ಸಹಾಯ' or 'education loan'"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit" className="hero-search-btn" disabled={loading}>
              {loading ? <div className="spinner"></div> : "Search"}
            </button>
          </div>
        </form>
      </div>

      {error && <div className="no-match animate-fade-in">{error}</div>}

      {results.length > 0 && (
        <div className="results-list animate-fade-in">
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

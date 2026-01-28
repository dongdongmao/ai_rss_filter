import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FilterPanel from './components/FilterPanel';
import ResultsPanel from './components/ResultsPanel';
import ConfigPanel from './components/ConfigPanel';
import './App.css';

// Use relative path for production, fallback to localhost for development
const API_URL = process.env.REACT_APP_API_URL || '/api';

function App() {
  const [activeTab, setActiveTab] = useState('filter');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [config, setConfig] = useState(null);
  const [error, setError] = useState(null);
  const [lastArticles, setLastArticles] = useState([]);

  const [filterParams, setFilterParams] = useState({
    confidence_threshold: 0.7,
    min_content_length: 50,
    spam_threshold: 0.4,
    max_articles: 10
  });

  // Load configuration on mount
  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await axios.get(`${API_URL}/config`);
      setConfig(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load configuration');
      console.error(err);
    }
  };

  const handleFilter = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/filter`, filterParams);
      setResults(response.data);
      setLastArticles(response.data.articles);
    } catch (err) {
      setError('Failed to run filter: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSendTelegram = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/notify/telegram`, {
        articles: lastArticles
      });
      alert(response.data.message);
    } catch (err) {
      setError('Failed to send to Telegram: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSendEmail = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/notify/email`, {
        articles: lastArticles
      });
      alert(response.data.message);
    } catch (err) {
      setError('Failed to send email: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 Personal RSS Denoiser</h1>
        <p>Intelligent RSS filtering powered by AI</p>
      </header>

      <div className="app-container">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'filter' ? 'active' : ''}`}
            onClick={() => setActiveTab('filter')}
          >
            🚀 Run Filter
          </button>
          <button
            className={`tab ${activeTab === 'notify' ? 'active' : ''}`}
            onClick={() => setActiveTab('notify')}
          >
            📱 Notifications
          </button>
          <button
            className={`tab ${activeTab === 'config' ? 'active' : ''}`}
            onClick={() => setActiveTab('config')}
          >
            ⚙️ Configuration
          </button>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <div className="tab-content">
          {activeTab === 'filter' && (
            <div className="filter-section">
              <FilterPanel
                params={filterParams}
                onChange={setFilterParams}
                onFilter={handleFilter}
                loading={loading}
              />
              {results && (
                <ResultsPanel
                  results={results}
                  onSendTelegram={handleSendTelegram}
                  onSendEmail={handleSendEmail}
                  loading={loading}
                />
              )}
            </div>
          )}

          {activeTab === 'notify' && (
            <div className="notify-section">
              <h2>📱 Send Notifications</h2>
              {lastArticles.length === 0 ? (
                <p>No articles to send. Run filter first!</p>
              ) : (
                <div className="notify-buttons">
                  <button
                    className="btn btn-primary"
                    onClick={handleSendTelegram}
                    disabled={loading}
                  >
                    📱 Send to Telegram ({lastArticles.length} articles)
                  </button>
                  <button
                    className="btn btn-primary"
                    onClick={handleSendEmail}
                    disabled={loading}
                  >
                    ✉️ Send Email ({lastArticles.length} articles)
                  </button>
                </div>
              )}
            </div>
          )}

          {activeTab === 'config' && (
            <ConfigPanel config={config} onRefresh={loadConfig} />
          )}
        </div>
      </div>

      <footer className="app-footer">
        <p>🔗 Personal RSS Filter | Powered by React + FastAPI</p>
      </footer>
    </div>
  );
}

export default App;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FilterPanel from './components/FilterPanel';
import ResultsPanel from './components/ResultsPanel';
import ConfigPanel from './components/ConfigPanel';
import './App.css';

// Use relative path for production, fallback to localhost for development
const API_URL = process.env.REACT_APP_API_URL || '/api';

// Filter can take long (model load + RSS fetch + classification). Avoid BodyStreamBuffer aborted / timeout.
const FILTER_TIMEOUT_MS = 5 * 60 * 1000; // 5 minutes
const CONFIG_TIMEOUT_MS = 30 * 1000;    // 30 seconds

function getErrorMessage(err) {
  const msg = err.response?.data?.detail ?? err.message ?? 'Unknown error';
  if (msg.includes('aborted') || msg.includes('BodyStreamBuffer') || err.code === 'ECONNABORTED') {
    return 'Request was cancelled or timed out. The filter may take 1–2 minutes (model loading). Please try again and wait.';
  }
  return msg;
}

function App() {
  const [activeTab, setActiveTab] = useState('filter');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [config, setConfig] = useState(null);
  const [error, setError] = useState(null);
  const [lastArticles, setLastArticles] = useState([]);
  const [inputMode, setInputMode] = useState('rss'); // 'rss' or 'manual'
  const [manualArticles, setManualArticles] = useState([
    { title: '', content: '', link: '', source: 'Manual Input' }
  ]);

  const [selectedTopics, setSelectedTopics] = useState([]);
  const [maxArticles, setMaxArticles] = useState(10);

  // Load configuration on mount
  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await axios.get(`${API_URL}/config`, { timeout: CONFIG_TIMEOUT_MS });
      setConfig(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load configuration: ' + getErrorMessage(err));
      console.error(err);
    }
  };

  const handleFilter = async () => {
    setLoading(true);
    setError(null);
    try {
      let response;
      if (inputMode === 'manual') {
        // Filter manually entered articles
        const articlesToFilter = manualArticles.filter(a => a.title.trim() && a.content.trim());
        if (articlesToFilter.length === 0) {
          setError('Please enter at least one article with title and content');
          setLoading(false);
          return;
        }
        response = await axios.post(`${API_URL}/filter/manual`, {
          articles: articlesToFilter,
          max_articles: maxArticles
        }, { timeout: FILTER_TIMEOUT_MS });
      } else {
        response = await axios.post(`${API_URL}/filter`, {
          topics: selectedTopics,
          max_articles: maxArticles
        }, { timeout: FILTER_TIMEOUT_MS });
      }
      setResults(response.data);
      setLastArticles(response.data.articles);
    } catch (err) {
      setError('Failed to run filter: ' + getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const addManualArticle = () => {
    setManualArticles([...manualArticles, { title: '', content: '', link: '', source: 'Manual Input' }]);
  };

  const removeManualArticle = (index) => {
    setManualArticles(manualArticles.filter((_, i) => i !== index));
  };

  const updateManualArticle = (index, field, value) => {
    const updated = [...manualArticles];
    updated[index][field] = value;
    setManualArticles(updated);
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
              <div style={{ marginBottom: '20px', padding: '15px', background: '#f5f5f5', borderRadius: '8px' }}>
                <label style={{ marginRight: '15px', fontWeight: 'bold' }}>Input Mode:</label>
                <button
                  className={`btn ${inputMode === 'rss' ? 'btn-primary' : ''}`}
                  onClick={() => setInputMode('rss')}
                  style={{ marginRight: '10px' }}
                >
                  📡 RSS Feeds
                </button>
                <button
                  className={`btn ${inputMode === 'manual' ? 'btn-primary' : ''}`}
                  onClick={() => setInputMode('manual')}
                >
                  ✍️ Manual Input
                </button>
                {inputMode === 'rss' && (
                  <p style={{ marginTop: '10px', fontSize: '0.9em', color: '#666' }}>
                    Note: If RSS feeds are unavailable (e.g., on Hugging Face Spaces), demo articles will be used automatically.
                  </p>
                )}
              </div>

              {inputMode === 'manual' && (
                <div style={{ marginBottom: '20px', padding: '15px', background: '#fff', border: '1px solid #ddd', borderRadius: '8px' }}>
                  <h3>Enter Articles Manually</h3>
                  {manualArticles.map((article, index) => (
                    <div key={index} style={{ marginBottom: '15px', padding: '15px', background: '#f9f9f9', borderRadius: '5px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                        <strong>Article {index + 1}</strong>
                        {manualArticles.length > 1 && (
                          <button
                            className="btn"
                            onClick={() => removeManualArticle(index)}
                            style={{ background: '#ff4444', color: 'white', padding: '5px 10px' }}
                          >
                            Remove
                          </button>
                        )}
                      </div>
                      <input
                        type="text"
                        placeholder="Article Title *"
                        value={article.title}
                        onChange={(e) => updateManualArticle(index, 'title', e.target.value)}
                        style={{ width: '100%', padding: '8px', marginBottom: '10px', borderRadius: '4px', border: '1px solid #ddd' }}
                      />
                      <textarea
                        placeholder="Article Content *"
                        value={article.content}
                        onChange={(e) => updateManualArticle(index, 'content', e.target.value)}
                        rows="3"
                        style={{ width: '100%', padding: '8px', marginBottom: '10px', borderRadius: '4px', border: '1px solid #ddd' }}
                      />
                      <input
                        type="text"
                        placeholder="Link (optional)"
                        value={article.link}
                        onChange={(e) => updateManualArticle(index, 'link', e.target.value)}
                        style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
                      />
                    </div>
                  ))}
                  <button
                    className="btn"
                    onClick={addManualArticle}
                    style={{ background: '#4CAF50', color: 'white' }}
                  >
                    + Add Another Article
                  </button>
                </div>
              )}

              <FilterPanel
                topics={config?.categories ?? []}
                selectedTopics={selectedTopics}
                onSelectTopics={setSelectedTopics}
                maxArticles={maxArticles}
                onMaxArticlesChange={setMaxArticles}
                onFilter={handleFilter}
                loading={loading}
              />
              {results && (
                <ResultsPanel
                  results={results}
                  loading={loading}
                />
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

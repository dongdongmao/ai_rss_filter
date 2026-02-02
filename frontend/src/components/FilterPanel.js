import React from 'react';
import './FilterPanel.css';

const TOPIC_LABELS = {
  tech: 'Technology',
  ai: 'AI / ML',
  crypto: 'Crypto',
  general: 'General'
};

function FilterPanel({ topics = [], selectedTopics = [], onSelectTopics, maxArticles, onMaxArticlesChange, onFilter, loading }) {
  const handleToggle = (topic) => {
    const next = selectedTopics.includes(topic)
      ? selectedTopics.filter((t) => t !== topic)
      : [...selectedTopics, topic];
    onSelectTopics(next);
  };

  const handleSelectAll = () => {
    onSelectTopics(topics.length ? [...topics] : []);
  };

  const handleClearAll = () => {
    onSelectTopics([]);
  };

  return (
    <div className="filter-panel">
      <h2>Select Topics</h2>
      <p className="filter-hint">Choose topics to filter content. Leave all unchecked to show all.</p>

      <div className="topics-group">
        <div className="topics-actions">
          <button type="button" className="btn-link" onClick={handleSelectAll}>Select all</button>
          <span className="sep">|</span>
          <button type="button" className="btn-link" onClick={handleClearAll}>Clear</button>
        </div>
        <div className="topic-checkboxes">
          {topics.length === 0 ? (
            <p className="no-topics">Loading topics…</p>
          ) : (
            topics.map((topic) => (
              <label key={topic} className="topic-check">
                <input
                  type="checkbox"
                  checked={selectedTopics.includes(topic)}
                  onChange={() => handleToggle(topic)}
                />
                <span>{TOPIC_LABELS[topic] || topic}</span>
              </label>
            ))
          )}
        </div>
      </div>

      <div className="control-group">
        <label>Max articles to show</label>
        <select
          value={maxArticles}
          onChange={(e) => onMaxArticlesChange(Number(e.target.value))}
        >
          {[5, 10, 15, 20, 30, 50].map((n) => (
            <option key={n} value={n}>{n}</option>
          ))}
        </select>
      </div>

      <button
        className="btn btn-large"
        onClick={onFilter}
        disabled={loading}
      >
        {loading ? '⏳ Running...' : '▶️ Run Filter'}
      </button>
    </div>
  );
}

export default FilterPanel;

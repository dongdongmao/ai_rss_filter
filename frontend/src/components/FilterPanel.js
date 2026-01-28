import React from 'react';
import './FilterPanel.css';

function FilterPanel({ params, onChange, onFilter, loading }) {
  const handleChange = (field, value) => {
    onChange({
      ...params,
      [field]: value
    });
  };

  return (
    <div className="filter-panel">
      <h2>Adjust Filter Parameters</h2>
      
      <div className="control-group">
        <label>
          Classification Confidence Threshold: {params.confidence_threshold.toFixed(2)}
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={params.confidence_threshold}
          onChange={(e) => handleChange('confidence_threshold', parseFloat(e.target.value))}
        />
      </div>

      <div className="control-group">
        <label>
          Spam Score Threshold: {params.spam_threshold.toFixed(2)}
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={params.spam_threshold}
          onChange={(e) => handleChange('spam_threshold', parseFloat(e.target.value))}
        />
      </div>

      <div className="control-group">
        <label>
          Minimum Content Length: {params.min_content_length} chars
        </label>
        <input
          type="range"
          min="10"
          max="500"
          step="10"
          value={params.min_content_length}
          onChange={(e) => handleChange('min_content_length', parseInt(e.target.value))}
        />
      </div>

      <div className="control-group">
        <label>
          Maximum Articles to Display: {params.max_articles}
        </label>
        <input
          type="range"
          min="1"
          max="50"
          step="1"
          value={params.max_articles}
          onChange={(e) => handleChange('max_articles', parseInt(e.target.value))}
        />
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

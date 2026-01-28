import React from 'react';
import './ConfigPanel.css';

function ConfigPanel({ config, onRefresh }) {
  if (!config) {
    return <div className="config-panel">Loading configuration...</div>;
  }

  return (
    <div className="config-panel">
      <div className="config-header">
        <h2>⚙️ Configuration</h2>
        <button className="btn-refresh" onClick={onRefresh}>
          🔄 Refresh
        </button>
      </div>

      <div className="config-section">
        <h3>🔗 RSS Sources</h3>
        <p className="config-info">Total: {config.sources.length} | Enabled: {config.sources.filter(s => s.enabled).length}</p>
        <div className="sources-list">
          {config.sources.map((source, index) => (
            <div key={index} className={`source-item ${source.enabled ? 'enabled' : 'disabled'}`}>
              <span className="status">{source.enabled ? '✅' : '❌'}</span>
              <span className="name">{source.name}</span>
              <span className="category">{source.category}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="config-section">
        <h3>🤖 Model Configuration</h3>
        <div className="config-item">
          <span className="label">Model:</span>
          <span className="value">{config.model_name}</span>
        </div>
        <div className="config-item">
          <span className="label">Device:</span>
          <span className="value">{config.device}</span>
        </div>
      </div>

      <div className="config-section">
        <h3>🎯 Filter Parameters</h3>
        <div className="config-item">
          <span className="label">Confidence Threshold:</span>
          <span className="value">{config.confidence_threshold}</span>
        </div>
        <div className="config-item">
          <span className="label">Minimum Content Length:</span>
          <span className="value">{config.min_content_length} chars</span>
        </div>
        <div className="config-item">
          <span className="label">Spam Score Threshold:</span>
          <span className="value">{config.spam_threshold}</span>
        </div>
      </div>

      <div className="config-tip">
        <p>
          💡 <strong>Tip:</strong> To add or modify RSS sources, edit the 
          <code>config/rss_sources.json</code> file and refresh.
        </p>
      </div>
    </div>
  );
}

export default ConfigPanel;

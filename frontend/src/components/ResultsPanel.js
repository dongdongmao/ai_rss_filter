import React from 'react';
import './ResultsPanel.css';

function ResultsPanel({ results, loading }) {
  return (
    <div className="results-panel">
      <h2>✅ Filtering Completed!</h2>
      
      <div className="statistics">
        <div className="stat-box">
          <div className="stat-number">{results.total_fetched}</div>
          <div className="stat-label">Fetched</div>
        </div>
        <div className="stat-box">
          <div className="stat-number">{results.filtered_count}</div>
          <div className="stat-label">Filtered</div>
        </div>
        <div className="stat-box">
          <div className="stat-number">{results.final_count}</div>
          <div className="stat-label">Final</div>
        </div>
      </div>

      <div className="articles-list">
        <h3>📰 Articles ({results.final_count})</h3>
        {results.articles.length === 0 ? (
          <p className="no-articles">No articles matched the filter criteria.</p>
        ) : (
          results.articles.map((article, index) => (
            <div key={index} className="article-card">
              <div className="article-header">
                <h4>{index + 1}. {article.title}</h4>
              </div>
              <div className="article-meta">
                {article.topic && <span className="badge topic">📂 {article.topic}</span>}
                <span className="badge">📌 {article.source}</span>
                <span className="badge quality">⭐ {(article.quality_score * 100).toFixed(0)}%</span>
                <span className="badge spam">🚫 {(article.spam_score * 100).toFixed(0)}%</span>
              </div>
              <p className="article-content">{(article.content || '').substring(0, 150)}{(article.content || '').length > 150 ? '...' : ''}</p>
              <div className="article-footer">
                <a href={article.link} target="_blank" rel="noopener noreferrer" className="read-more">
                  Read More →
                </a>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ResultsPanel;

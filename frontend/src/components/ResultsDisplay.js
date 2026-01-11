import React from 'react';
import './ResultsDisplay.css';

const ResultsDisplay = ({ results }) => {
  if (!results || !results.success) {
    return null;
  }

  const getSeverityClass = (prediction) => {
    const pred = prediction.toLowerCase();
    if (pred.includes('high')) return 'severity-high';
    if (pred.includes('moderate')) return 'severity-moderate';
    if (pred.includes('low')) return 'severity-low';
    return 'severity-none';
  };

  const getSeverityIcon = (prediction) => {
    const pred = prediction.toLowerCase();
    if (pred.includes('high')) return '🔴';
    if (pred.includes('moderate')) return '🟡';
    if (pred.includes('low')) return '🟢';
    return '✅';
  };

  const severityClass = getSeverityClass(results.prediction);
  const severityIcon = getSeverityIcon(results.prediction);

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Analysis Results</h2>
      </div>

      <div className={`prediction-card ${severityClass}`}>
        <div className="prediction-header">
          <span className="severity-icon">{severityIcon}</span>
          <h3 className="prediction-title">
            {results.prediction} Dark Circles
          </h3>
          {results.confidence && (
            <span className="confidence-badge">
              {Math.round(results.confidence * 100)}% confidence
            </span>
          )}
        </div>
      </div>

      <div className="advice-section">
        <div className="advice-card causes-card">
          <h4 className="advice-title">
            <span className="advice-icon">🔍</span>
            Possible Causes
          </h4>
          <p className="advice-content">{results.causes}</p>
        </div>

        <div className="advice-card remedies-card">
          <h4 className="advice-title">
            <span className="advice-icon">💡</span>
            Recommended Remedies
          </h4>
          <div className="advice-content remedies-list">
            {results.remedies.split('\n').map((remedy, index) => (
              <div key={index} className="remedy-item">
                {remedy.trim()}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;


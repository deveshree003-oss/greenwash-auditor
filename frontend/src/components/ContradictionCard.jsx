import SourceBadge from './SourceBadge';

function confidenceLevel(value) {
  if (value >= 0.85) return 'high';
  if (value >= 0.7) return 'medium';
  return 'low';
}

export default function ContradictionCard({ item, index }) {
  const confidence = confidenceLevel(item.confidence);

  return (
    <article className="contradiction-card">
      <div className="contradiction-head">
        <div className="stack">
          <span className="tiny-label">Contradiction {index + 1}</span>
          <h3>{item.title}</h3>
        </div>
        <div className="stack" style={{ justifyItems: 'end' }}>
          <span className={`severity-chip ${item.severity}`}>{item.severity} severity</span>
          <span className={`confidence-pill ${confidence}`}>{Math.round(item.confidence * 100)}% confidence</span>
        </div>
      </div>

      <div className="card-row">
        {item.regulations.map((tag) => (
          <span key={tag} className="tag">
            {tag}
          </span>
        ))}
      </div>

      <div className="evidence-grid">
        <div className="evidence-block">
          <div className="card-row">
            <SourceBadge label={item.claimSource} />
            <span className="tiny-label">{item.claimCitation}</span>
          </div>
          <p>{item.claim}</p>
        </div>

        <div className="evidence-block">
          <div className="card-row">
            <SourceBadge label={item.evidenceSource} />
            <span className="tiny-label">{item.evidenceCitation}</span>
          </div>
          <p>{item.evidence}</p>
        </div>
      </div>

      <details>
        <summary className="ghost-button">Why this is risky</summary>
        <div className="legal-brief">
          <p>{item.whyItMatters}</p>
        </div>
      </details>
    </article>
  );
}

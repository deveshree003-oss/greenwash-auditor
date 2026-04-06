import SourceBadge from './SourceBadge';

function confidenceLevel(value) {
  if (value >= 0.85) return 'high';
  if (value >= 0.7) return 'medium';
  return 'low';
}

export default function ContradictionCard({ item, index }) {
  const confValue = typeof item.confidence === 'number' ? item.confidence : 0;
  const confidence = confidenceLevel(confValue);

  const regs = Array.isArray(item.regulations) ? item.regulations : [];
  const severity = item.severity || 'unknown';
  const title = item.title || item.claim || `Contradiction ${index + 1}`;

  return (
    <article className="contradiction-card">
      <div className="contradiction-head">
        <div className="stack">
          <span className="tiny-label">Contradiction {index + 1}</span>
          <h3>{title}</h3>
        </div>
        <div className="stack" style={{ justifyItems: 'end' }}>
          <span className={`severity-chip ${severity}`}>{severity} severity</span>
          <span className={`confidence-pill ${confidence}`}>{Math.round(confValue * 100)}% confidence</span>
        </div>
      </div>

      <div className="card-row">
        {regs.map((tag, i) => (
          <span key={`${tag || 'tag'}-${i}`} className="tag">
            {tag}
          </span>
        ))}
      </div>

      {/* quick visible explanation for debugging & UX: show short whyItMatters preview */}
      {item.whyItMatters ? (
        <div className="why-brief" style={{ marginTop: '12px', color: 'var(--muted)' }}>
          <strong>Why this matters:</strong> {item.whyItMatters}
        </div>
      ) : null}

      <div className="evidence-grid">
        <div className="evidence-block">
          <div className="card-row">
            <SourceBadge label={item.claimSource || ''} />
            <span className="tiny-label">{item.claimCitation || ''}</span>
          </div>
          <p>{item.claim || ''}</p>
        </div>

        <div className="evidence-block">
          <div className="card-row">
            <SourceBadge label={item.evidenceSource || ''} />
            <span className="tiny-label">{item.evidenceCitation || ''}</span>
          </div>
          <p>{item.evidence || ''}</p>
        </div>
      </div>

      <details>
        <summary className="ghost-button">Why this is risky</summary>
        <div className="legal-brief">
          <p>{item.whyItMatters || ''}</p>
        </div>
      </details>
    </article>
  );
}

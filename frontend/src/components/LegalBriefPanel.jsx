export default function LegalBriefPanel({ brief }) {
  return (
    <section className="panel">
      <div className="panel-body">
        <div className="section-header">
          <div className="stack">
            <span className="eyebrow">Regulatory Lens</span>
            <h2 className="section-title">Legal Briefing</h2>
          </div>
        </div>

        <div className="legal-brief">
          <p>{brief.summary}</p>
          <div className="card-row">
            {brief.regulations.map((regulation) => (
              <span key={regulation} className="tag">
                {regulation}
              </span>
            ))}
          </div>
        </div>

        <div className="legal-brief">
          <span className="tiny-label">Recommended actions</span>
          <ul>
            {brief.actions.map((action) => (
              <li key={action}>{action}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}

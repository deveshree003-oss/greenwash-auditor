export default function Timeline({ items }) {
  return (
    <section className="panel">
      <div className="panel-body">
        <div className="section-header">
          <div className="stack">
            <span className="eyebrow">Evidence Flow</span>
            <h2 className="section-title">Timeline of Signal Escalation</h2>
          </div>
        </div>

        <div className="timeline-list">
          {items.map((item) => (
            <div className="timeline-item" key={`${item.year}-${item.label}`}>
              <div className="timeline-year">{item.year}</div>
              <div>
                <h3 className="panel-title">{item.label}</h3>
                <p>{item.detail}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

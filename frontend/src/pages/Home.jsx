import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAvailableCompanies, runAudit } from '../api/client';

const featuredCompanies = getAvailableCompanies();

const initialForm = {
  company: 'Adani Green',
  csrUrl: '',
  tenKUrl: '',
  csrFile: null,
  tenKFile: null,
};

export default function Home() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState(null);

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setStatus(null);

    try {
      const result = await runAudit(form);
      const targetId = result.reportId || result.report?.id || 'adani';
      setStatus(
        result.mock
          ? 'Backend unavailable, so the UI loaded the high-fidelity demo report.'
          : 'Audit completed and routed into the live report view.',
      );
      navigate(`/report/${targetId}`, {
        state: {
          prefetchedReport: result.report,
          isMock: result.mock,
        },
      });
    } catch (error) {
      setStatus(error.message || 'Audit failed.');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="stack">
      <section className="hero hero-single">
        <div className="panel hero-copy">
          <div className="eyebrow">Agentic ESG Integrity Auditing</div>
          <h1>Catch greenwashing before investors do.</h1>
          <p>
            AI that cross-checks ESG claims with real filings in seconds.
          </p>

          <div className="hero-actions">
            <a href="#audit-intake" className="button">
              🚀 Run Audit
            </a>
            <button
              type="button"
              className="button-secondary"
              onClick={() => navigate('/report/adani')}
            >
              📊 View Demo
            </button>
          </div>

          <div className="hero-metrics">
            <div className="metric-card">
              <span className="tiny-label">Contradictions surfaced</span>
              <strong>3-5+</strong>
            </div>
            <div className="metric-card">
              <span className="tiny-label">Risk index</span>
              <strong>1-100</strong>
            </div>
            <div className="metric-card">
              <span className="tiny-label">Reg tags</span>
              <strong>EU / SEBI</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="section-block">
        <div className="section-header">
          <div className="stack">
            <span className="eyebrow">How It Works</span>
            <h2 className="section-title">Three steps from report to red flag</h2>
          </div>
        </div>

        <div className="workflow-grid">
          <article className="workflow-step">
            <div className="workflow-icon">📄</div>
            <h3>Upload Reports</h3>
            <p>Drop in the CSR report and 10-K or paste source URLs for instant intake.</p>
          </article>
          <article className="workflow-step">
            <div className="workflow-icon">🤖</div>
            <h3>AI Scans &amp; Compares</h3>
            <p>Agentic reasoning extracts claims, financial disclosures, and supporting citations.</p>
          </article>
          <article className="workflow-step">
            <div className="workflow-icon">⚠️</div>
            <h3>Flags Contradictions</h3>
            <p>Risk scoring, regulation mapping, and evidence cards expose where the story breaks.</p>
          </article>
        </div>
      </section>

      <section className="section-block">
        <div className="section-header">
          <div className="stack">
            <span className="eyebrow">Core Engine</span>
            <h2 className="section-title">Built to look like a serious compliance weapon</h2>
          </div>
        </div>

        <div className="feature-grid">
          <article className="feature-card">
            <div className="workflow-icon">🔍</div>
            <h3>Contradiction Detection</h3>
            <p>Matches glossy ESG claims against filings, notes, incidents, and external disclosures.</p>
          </article>
          <article className="feature-card">
            <div className="workflow-icon">📈</div>
            <h3>Risk Scoring Engine</h3>
            <p>Ranks each case with a 1-100 severity signal so judges immediately see impact.</p>
          </article>
          <article className="feature-card">
            <div className="workflow-icon">📑</div>
            <h3>Regulatory Mapping</h3>
            <p>Maps every contradiction to SEBI BRSR and EU Taxonomy exposure tags.</p>
          </article>
          <article className="feature-card">
            <div className="workflow-icon">⚖️</div>
            <h3>Compliance Alerts</h3>
            <p>Summarizes legal risk in plain language for audit, analyst, and investor review.</p>
          </article>
        </div>
      </section>

      <section id="audit-intake" className="panel section-block">
        <div className="panel-body">
          <div className="section-header">
            <div className="stack">
              <span className="eyebrow">Audit Intake</span>
              <h2 className="section-title">Upload source material or audit from URLs</h2>
            </div>
          </div>

          {status ? <div className="status-banner">{status}</div> : null}

          <form className="stack" onSubmit={handleSubmit}>
            <div className="input-grid">
              <div className="field">
                <label htmlFor="company">Company or target entity</label>
                <input
                  id="company"
                  value={form.company}
                  onChange={(event) => updateField('company', event.target.value)}
                  placeholder="Adani Green"
                />
              </div>

              <div className="field">
                <label htmlFor="csr-url">CSR / sustainability report URL</label>
                <input
                  id="csr-url"
                  value={form.csrUrl}
                  onChange={(event) => updateField('csrUrl', event.target.value)}
                  placeholder="https://example.com/csr.pdf"
                />
              </div>

              <div className="field">
                <label htmlFor="tenk-url">10-K / annual filing URL</label>
                <input
                  id="tenk-url"
                  value={form.tenKUrl}
                  onChange={(event) => updateField('tenKUrl', event.target.value)}
                  placeholder="https://example.com/10k.pdf"
                />
              </div>

              <div className="field">
                <label htmlFor="notes">Analyst note</label>
                <textarea
                  id="notes"
                  value="Focus on emissions, capex alignment, and any mismatch between public claims and filing disclosures."
                  readOnly
                />
              </div>
            </div>

            <div className="input-grid">
              <label className="dropzone">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(event) => updateField('csrFile', event.target.files?.[0] || null)}
                />
                <span className="tiny-label">Drop or browse</span>
                <strong>Upload CSR / ESG PDF</strong>
                <span className="support-text">
                  Supports sustainability reports, BRSR filings, or investor ESG decks.
                </span>
                {form.csrFile ? <span className="file-chip">{form.csrFile.name}</span> : null}
              </label>

              <label className="dropzone">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(event) => updateField('tenKFile', event.target.files?.[0] || null)}
                />
                <span className="tiny-label">Drop or browse</span>
                <strong>Upload 10-K / annual filing PDF</strong>
                <span className="support-text">
                  Use annual reports, statutory disclosures, or financial statement packs.
                </span>
                {form.tenKFile ? <span className="file-chip">{form.tenKFile.name}</span> : null}
              </label>
            </div>

            <div className="inline-actions">
              <button type="submit" className="button" disabled={isSubmitting}>
                {isSubmitting ? 'Running audit...' : 'Run contradiction audit'}
              </button>
              <button
                type="button"
                className="ghost-button"
                onClick={() => navigate('/compare')}
              >
                Open compare mode
              </button>
            </div>
          </form>
        </div>
      </section>

      <section className="section-block">
        <div className="section-header">
          <div className="stack">
            <span className="eyebrow">Benchmark Set</span>
            <h2 className="section-title">Prototype-ready comparison companies</h2>
          </div>
        </div>

        <div className="compare-grid">
          {featuredCompanies.map((company) => (
            <article key={company.id} className="compare-card">
              <div className="compare-card-head">
                <div className="stack">
                  <h3>{company.company}</h3>
                  <span className="tiny-label">{company.sector}</span>
                </div>
                <span className={`severity-chip ${company.riskScore >= 75 ? 'high' : company.riskScore >= 50 ? 'medium' : 'low'}`}>
                  {company.riskScore}/100
                </span>
              </div>
              <p>
                Use this mock entity to stress-test the dashboard, comparison page,
                and downloadable summary flow.
              </p>
              <div className="inline-actions">
                <button
                  type="button"
                  className="button-secondary"
                  onClick={() => navigate(`/report/${company.id}`)}
                >
                  Open report
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

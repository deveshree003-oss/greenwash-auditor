import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { fetchComparison, getAvailableCompanies } from '../api/client';

const allCompanies = getAvailableCompanies();

export default function Compare() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSelection = searchParams.get('ids')?.split(',').filter(Boolean) || ['adani', 'reliance'];
  const [selectedIds, setSelectedIds] = useState(initialSelection);
  const [reports, setReports] = useState([]);

  useEffect(() => {
    let active = true;

    async function load() {
      const result = await fetchComparison(selectedIds);
      if (active) {
        setReports(result);
      }
    }

    load();
    setSearchParams({ ids: selectedIds.join(',') });

    return () => {
      active = false;
    };
  }, [selectedIds, setSearchParams]);

  function toggleSelection(id) {
    setSelectedIds((current) => {
      if (current.includes(id)) {
        return current.length === 1 ? current : current.filter((item) => item !== id);
      }

      if (current.length >= 3) {
        return [...current.slice(1), id];
      }

      return [...current, id];
    });
  }

  return (
    <div className="stack">
      <section className="page-header panel">
        <div className="panel-body">
          <div className="eyebrow">Multi-company View</div>
          <h1>Compare greenwashing risk posture across companies.</h1>
          <p>
            Use this view to show investors, compliance teams, or judges how the
            contradiction engine prioritizes severity, evidence, and regulatory
            exposure across multiple issuers.
          </p>
        </div>
      </section>

      <section className="panel">
        <div className="panel-body">
          <div className="section-header">
            <div className="stack">
              <span className="eyebrow">Selection</span>
              <h2 className="section-title">Pick up to three companies</h2>
            </div>
          </div>

          <div className="card-row">
            {allCompanies.map((company) => {
              const active = selectedIds.includes(company.id);
              return (
                <button
                  type="button"
                  key={company.id}
                  className={active ? 'button-secondary' : 'ghost-button'}
                  onClick={() => toggleSelection(company.id)}
                >
                  {company.company}
                </button>
              );
            })}
          </div>
        </div>
      </section>

      <section className="compare-grid">
        {reports.map((report) => (
          <article key={report.id} className="compare-card">
            <div className="compare-card-head">
              <div className="stack">
                <h3>{report.company}</h3>
                <span className="tiny-label">{report.sector}</span>
              </div>
              <span
                className={`severity-chip ${
                  report.riskScore >= 75 ? 'high' : report.riskScore >= 50 ? 'medium' : 'low'
                }`}
              >
                {report.riskScore}/100
              </span>
            </div>

            <p>{report.executiveSummary}</p>

            <div className="stat-grid">
              <div className="stat">
                <span className="stat-label">Contradictions</span>
                <strong>{report.stats.contradictions}</strong>
              </div>
              <div className="stat">
                <span className="stat-label">Reg tags</span>
                <strong>{report.legalBrief.regulations.length}</strong>
              </div>
            </div>

            <div className="legal-brief">
              <span className="tiny-label">Highest signal</span>
              <p>{report.contradictions[0]?.title || 'No severe contradiction captured in the mock set.'}</p>
            </div>

            <div className="legal-brief">
              <span className="tiny-label">Legal lens</span>
              <ul>
                {report.legalBrief.regulations.map((rule) => (
                  <li key={rule}>{rule}</li>
                ))}
              </ul>
            </div>

            <div className="inline-actions">
              <button
                type="button"
                className="button"
                onClick={() => navigate(`/report/${report.id}`)}
              >
                Open full report
              </button>
            </div>
          </article>
        ))}
      </section>

      <p className="footer-note">
        Comparison uses mock-backed report objects now and can switch to live
        backend results as soon as the shared API exposes comparison-ready data.
      </p>
    </div>
  );
}

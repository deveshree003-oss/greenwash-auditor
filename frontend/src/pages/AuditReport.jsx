import { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { downloadAuditSummary, fetchReport } from '../api/client';
import ContradictionCard from '../components/ContradictionCard';
import LegalBriefPanel from '../components/LegalBriefPanel';
import RiskScoreGauge from '../components/RiskScoreGauge';
import ScoreBreakdownChart from '../components/ScoreBreakdownChart';
import Timeline from '../components/Timeline';

export default function AuditReport() {
  const { companyId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [report, setReport] = useState(location.state?.prefetchedReport || null);
  const [isMock, setIsMock] = useState(Boolean(location.state?.isMock));
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;

    async function loadReport() {
      const result = await fetchReport(companyId);
      if (!active) return;
      setReport(result.report);
      setIsMock(Boolean(result.mock));
      setError(result.error || '');
    }

    if (!location.state?.prefetchedReport || location.state?.prefetchedReport.id !== companyId) {
      loadReport();
    }

    return () => {
      active = false;
    };
  }, [companyId, location.state]);

  if (!report) {
    return (
      <div className="panel">
        <div className="panel-body">
          <p>Loading audit report...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="stack">
      <section className="page-header panel">
        <div className="panel-body">
          <div className="eyebrow">Audit Dashboard</div>
          <h1>{report.company}</h1>
          <p>{report.executiveSummary}</p>

          <div className="report-actions">
            <button
              type="button"
              className="button"
              onClick={() => downloadAuditSummary(report)}
            >
              Download audit summary
            </button>
            <button
              type="button"
              className="button-secondary"
              onClick={() => navigate('/compare')}
            >
              Compare companies
            </button>
          </div>

          {isMock ? (
            <div className="status-banner">
              Demo data is active because the backend response was unavailable.
            </div>
          ) : null}
          {error && !isMock ? <div className="status-banner">{error}</div> : null}
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="left-rail">
          <section className="panel">
            <div className="panel-body">
              <div className="section-header">
                <div className="stack">
                  <span className="eyebrow">Risk Index</span>
                  <h2 className="section-title">Integrity score</h2>
                </div>
              </div>

              <RiskScoreGauge score={report.riskScore} />

              <div className="gauge-meta">
                <div className="stat-grid">
                  <div className="stat">
                    <span className="stat-label">Contradictions</span>
                    <strong>{report.stats.contradictions}</strong>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Docs scanned</span>
                    <strong>{report.stats.documentsScanned}</strong>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Reg exposure</span>
                    <strong>{report.stats.regulatoryExposure}</strong>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Flagged capex</span>
                    <strong>{report.stats.flaggedCapex}</strong>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <ScoreBreakdownChart breakdown={report.severityBreakdown} />
          <LegalBriefPanel brief={report.legalBrief} />
        </div>

        <div className="right-rail">
          <section className="panel">
            <div className="panel-body">
              <div className="section-header">
                <div className="stack">
                  <span className="eyebrow">Contradiction Evidence</span>
                  <h2 className="section-title">Flagged claim mismatches</h2>
                </div>
              </div>

              <div className="card-stack">
                {report.contradictions.length ? (
                  report.contradictions.map((item, index) => (
                    <ContradictionCard key={item.id} item={item} index={index} />
                  ))
                ) : (
                  <div className="surface">
                    <p>No contradiction cards are available for this mock report yet.</p>
                  </div>
                )}
              </div>
            </div>
          </section>

          <Timeline items={report.timeline} />

          <section className="panel">
            <div className="panel-body">
              <div className="section-header">
                <div className="stack">
                  <span className="eyebrow">External Context</span>
                  <h2 className="section-title">News and incident signals</h2>
                </div>
              </div>
              <ul className="mini-list">
                {report.news.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </section>
        </div>
      </section>
    </div>
  );
}

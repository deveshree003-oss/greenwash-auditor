import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from 'recharts';

export default function ScoreBreakdownChart({ breakdown }) {
  const data = Object.entries(breakdown).map(([subject, value]) => ({
    subject,
    value,
    fullMark: 100,
  }));

  return (
    <section className="panel">
      <div className="panel-body">
        <div className="section-header">
          <div className="stack">
            <span className="eyebrow">Severity Profile</span>
            <h2 className="section-title">Risk Breakdown</h2>
          </div>
        </div>

        <div className="chart-shell">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={data}>
              <PolarGrid stroke="rgba(142,165,183,0.18)" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: '#c5d4df', fontSize: 12 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#8ea5b7', fontSize: 11 }} />
              <Radar
                name="Risk"
                dataKey="value"
                stroke="#81e6d9"
                fill="#81e6d9"
                fillOpacity={0.26}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  );
}

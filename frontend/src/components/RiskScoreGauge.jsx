const SIZE = 240;
const STROKE = 18;
const RADIUS = (SIZE - STROKE) / 2;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

function getGaugeColor(score) {
  if (score >= 75) return '#ff7b72';
  if (score >= 50) return '#ffb86b';
  return '#81e6d9';
}

export default function RiskScoreGauge({ score }) {
  const progress = Math.max(0, Math.min(score, 100)) / 100;
  const dashOffset = CIRCUMFERENCE * (1 - progress);
  const color = getGaugeColor(score);

  return (
    <div className="gauge-wrap">
      <svg width={SIZE} height={SIZE} viewBox={`0 0 ${SIZE} ${SIZE}`} role="img" aria-label={`Risk score ${score} out of 100`}>
        <defs>
          <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#81e6d9" />
            <stop offset="55%" stopColor="#ffc06c" />
            <stop offset="100%" stopColor="#ff7b72" />
          </linearGradient>
        </defs>
        <circle
          cx={SIZE / 2}
          cy={SIZE / 2}
          r={RADIUS}
          fill="none"
          stroke="rgba(255,255,255,0.07)"
          strokeWidth={STROKE}
        />
        <circle
          cx={SIZE / 2}
          cy={SIZE / 2}
          r={RADIUS}
          fill="none"
          stroke="url(#gaugeGradient)"
          strokeWidth={STROKE}
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          strokeDashoffset={dashOffset}
          transform={`rotate(-90 ${SIZE / 2} ${SIZE / 2})`}
          style={{ transition: 'stroke-dashoffset 900ms ease' }}
        />
        <circle
          cx={SIZE / 2}
          cy={SIZE / 2}
          r={RADIUS - 32}
          fill="rgba(5, 11, 17, 0.85)"
          stroke="rgba(129,230,217,0.12)"
        />
        <text
          x="50%"
          y="48%"
          textAnchor="middle"
          fill={color}
          fontSize="52"
          fontWeight="700"
          fontFamily="Space Grotesk, sans-serif"
        >
          {score}
        </text>
        <text
          x="50%"
          y="60%"
          textAnchor="middle"
          fill="#8ea5b7"
          fontSize="13"
          fontFamily="IBM Plex Mono, monospace"
          style={{ textTransform: 'uppercase', letterSpacing: '0.16em' }}
        >
          risk index
        </text>
      </svg>
    </div>
  );
}

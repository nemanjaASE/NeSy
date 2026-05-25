const symptoms = [
  { className: "sym-shock", label: ["shock"], cx: 138, cy: 52 },
  { className: "sym-bloodshot", label: ["bloodshot", "eyes"], cx: 362, cy: 52 },
  { className: "sym-fever", label: ["fever"], cx: 442, cy: 190 },
  {
    className: "sym-abdominal",
    label: ["abdominal", "pain"],
    cx: 376,
    cy: 318,
  },
  { className: "sym-backache", label: ["backache"], cx: 250, cy: 354 },
  { className: "sym-rash", label: ["rash"], cx: 124, cy: 318 },
  { className: "sym-chills", label: ["chills"], cx: 58, cy: 190 },
];

const CENTER = { cx: 250, cy: 200 };

export function KnowledgeGraphVisual() {
  return (
    <aside
      className="knowledge-graph-visual"
      aria-label="Knowledge graph preview"
    >
      <svg
        className="kg-svg"
        viewBox="0 0 500 420"
        aria-hidden="true"
      >
        <defs>
          <marker
            id="arr"
            viewBox="0 0 10 10"
            refX="8"
            refY="5"
            markerWidth="5"
            markerHeight="5"
            orient="auto-start-reverse"
          >
            <path
              d="M2 1L8 5L2 9"
              fill="none"
              stroke="rgba(87,211,238,0.8)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </marker>
          <radialGradient id="gd" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#8fb7ff" />
            <stop offset="100%" stopColor="#5b7cfa" />
          </radialGradient>
          <radialGradient id="gs" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#a7f3d0" />
            <stop offset="100%" stopColor="#34d399" />
          </radialGradient>
          <filter id="glow-d">
            <feGaussianBlur stdDeviation="2.4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="glow-s">
            <feGaussianBlur stdDeviation="1.8" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* edges */}
        {symptoms.map((s) => (
          <line
            key={s.className}
            x1={CENTER.cx}
            y1={CENTER.cy}
            x2={s.cx}
            y2={s.cy}
            stroke="rgba(87,211,238,0.55)"
            strokeWidth="1.5"
            strokeDasharray="6 4"
            fill="none"
            markerEnd="url(#arr)"
          />
        ))}

        {/* disease node */}
        <g
          className="kg-float kg-float-main"
          filter="url(#glow-d)"
        >
          <circle cx="250" cy="200" r="68" fill="#5b7cfa" opacity="0.08" />
          <circle cx="250" cy="200" r="58" fill="url(#gd)" />
          <circle
            cx="250"
            cy="200"
            r="58"
            fill="none"
            stroke="rgba(255,255,255,0.18)"
            strokeWidth="1"
          />
          <text
            x="250"
            y="193"
            textAnchor="middle"
            fontSize="12"
            fontWeight="900"
            fill="#08111f"
            fontFamily="sans-serif"
          >
            Korean
          </text>
          <text
            x="250"
            y="208"
            textAnchor="middle"
            fontSize="12"
            fontWeight="900"
            fill="#08111f"
            fontFamily="sans-serif"
          >
            hemorrhagic
          </text>
          <text
            x="250"
            y="223"
            textAnchor="middle"
            fontSize="12"
            fontWeight="900"
            fill="#08111f"
            fontFamily="sans-serif"
          >
            fever
          </text>
        </g>

        {/* symptom nodes */}
        {symptoms.map((s, i) => (
          <g
            key={s.className}
            className="kg-float"
            filter="url(#glow-s)"
            style={{
              animationDelay: `${i * 0.18}s`,
              transformOrigin: `${s.cx}px ${s.cy}px`,
            }}
          >
            <circle cx={s.cx} cy={s.cy} r="40" fill="#34d399" opacity="0.08" />
            <circle cx={s.cx} cy={s.cy} r="35" fill="url(#gs)" />
            <circle
              cx={s.cx}
              cy={s.cy}
              r="35"
              fill="none"
              stroke="rgba(255,255,255,0.16)"
              strokeWidth="1"
            />
            {s.label.length === 1 ? (
              <text
                x={s.cx}
                y={s.cy + 4}
                textAnchor="middle"
                fontSize="12"
                fontWeight="900"
                fill="#062217"
                fontFamily="sans-serif"
              >
                {s.label[0]}
              </text>
            ) : (
              <>
                <text
                  x={s.cx}
                  y={s.cy - 3}
                  textAnchor="middle"
                  fontSize="11"
                  fontWeight="900"
                  fill="#062217"
                  fontFamily="sans-serif"
                >
                  {s.label[0]}
                </text>
                <text
                  x={s.cx}
                  y={s.cy + 10}
                  textAnchor="middle"
                  fontSize="11"
                  fontWeight="900"
                  fill="#062217"
                  fontFamily="sans-serif"
                >
                  {s.label[1]}
                </text>
              </>
            )}
          </g>
        ))}
      </svg>
    </aside>
  );
}

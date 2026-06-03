import { runtimePipeline } from "../model/content";

const stepIcons = ["text", "link", "graph", "score", "spark"];

function PipelineIcon({ type }: { type: string }) {
  if (type === "text") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M5 7h14M5 12h10M5 17h7" />
      </svg>
    );
  }

  if (type === "link") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M8 12h8M9 8l-4 4 4 4M15 8l4 4-4 4" />
      </svg>
    );
  }

  if (type === "graph") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="6" cy="12" r="2.5" />
        <circle cx="18" cy="7" r="2.5" />
        <circle cx="18" cy="17" r="2.5" />
        <path d="M8.2 10.9 15.8 8.1M8.2 13.1l7.6 2.8" />
      </svg>
    );
  }

  if (type === "score") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M5 19V9M12 19V5M19 19v-7M4 19h16" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3l1.7 5.1L19 10l-5.3 1.9L12 17l-1.7-5.1L5 10l5.3-1.9L12 3Z" />
      <path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8L19 15Z" />
    </svg>
  );
}

export function WorkflowSection() {
  return (
    <section className="workflow-section" id="workflow">
      <div className="workflow-intro">
        <span>Workflow</span>
        <h2>From narrative to explainable diagnostic reasoning.</h2>
        <p>
          Each diagnosis starts with the patient's own words, turns them into
          structured clinical findings, connects them to medical concepts, then
          ranks graph-backed candidates with a transparent explanation.
        </p>
      </div>

      <div className="workflow-panel">
        <div className="workflow-panel-header">
          <span>Runtime pipeline</span>
          <strong>What happens after Start diagnosis?</strong>
        </div>
        <div className="workflow-timeline">
          {runtimePipeline.map((card, index) => (
            <article
              className={`workflow-step workflow-step-${index + 1}`}
              key={card.title}
            >
              <span className="workflow-step-number">
                {String(index + 1).padStart(2, "0")}
              </span>
              <span className="workflow-step-icon">
                <PipelineIcon type={stepIcons[index]} />
              </span>
              <div>
                <small>{card.phase}</small>
                <h3>{card.title}</h3>
                <p>{card.text}</p>
                <strong>{card.artifact}</strong>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

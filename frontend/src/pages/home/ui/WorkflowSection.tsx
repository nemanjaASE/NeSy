import { runtimePipeline } from "../model/content";

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
              <div>
                <small>{card.phase}</small>
                <h3>{card.title}</h3>
                <p>{card.text}</p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

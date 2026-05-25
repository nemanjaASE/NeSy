import { workflowCards } from "../model/content";

export function WorkflowSection() {
  return (
    <section className="workflow" id="workflow">
      {workflowCards.map((card, index) => (
        <article className="workflow-card" key={card.title}>
          <div className="workflow-card-heading">
            <span>{String(index + 1).padStart(2, "0")}</span>
            <h2>{card.title}</h2>
          </div>
          <p>{card.text}</p>
        </article>
      ))}
    </section>
  );
}

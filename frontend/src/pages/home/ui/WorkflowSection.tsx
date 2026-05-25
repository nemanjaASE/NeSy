import { workflowCards } from "../model/content";

export function WorkflowSection() {
  return (
    <section className="workflow" id="workflow">
      {workflowCards.map((card) => (
        <article className="workflow-card" key={card.title}>
          <h2>{card.title}</h2>
          <p>{card.text}</p>
        </article>
      ))}
    </section>
  );
}

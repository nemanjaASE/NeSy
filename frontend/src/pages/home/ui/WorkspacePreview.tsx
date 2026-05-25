import { WindowControls } from "@/shared/ui/WindowControls/WindowControls";
import { findings } from "../model/content";

export function WorkspacePreview() {
  return (
    <section className="workspace" id="workspace">
      <div className="workspace-header">
        <WindowControls />
        <p>diagnosis.workspace</p>
      </div>

      <div className="workspace-grid">
        <div className="workspace-left">
          <article className="code-panel">
            <div className="panel-heading">
              <span>Patient narrative</span>
              <strong>Input</strong>
            </div>
            <p>
              I have a rash on my chest and arms. It itches and is red, but I
              have no fever, no fatigue, and no joint pain.
            </p>
          </article>

          <div className="finding-list">
            {findings.map((finding) => (
              <article
                className={`finding-card finding-card-${finding.tone}`}
                key={finding.label}
              >
                <div>
                  <small>{finding.label}</small>
                  <strong>{finding.value}</strong>
                </div>
              </article>
            ))}
          </div>
        </div>

        <div className="workspace-right">
          <article className="result-panel">
            <span className="panel-kicker">Explainable result</span>
            <h2>Contact dermatitis</h2>
            <p>
              Ranked as the leading candidate because the reported rash,
              itching, and redness align strongly, while systemic symptoms are
              explicitly absent.
            </p>

            <div className="confidence-card">
              <div>
                <span>Confidence</span>
                <strong>Medium</strong>
              </div>
              <div className="progress-track">
                <span />
              </div>
            </div>

            <div className="mini-grid">
              <div>
                <span>Differentials</span>
                <strong>eczema, urticaria</strong>
              </div>
              <div>
                <span>Verify</span>
                <strong>allergen exposure</strong>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  );
}

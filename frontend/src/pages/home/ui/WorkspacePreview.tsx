import { useState } from "react";
import { WindowControls } from "@/shared/ui/WindowControls/WindowControls";
import { previewDiagnosis } from "../model/content";

const findingCards = [
  {
    icon: "check",
    label: "Present",
    count: previewDiagnosis.presentSymptoms.length,
    status: "detected",
    items: previewDiagnosis.presentSymptoms,
    tone: "green",
  },
  {
    icon: "minus",
    label: "Absent",
    count: previewDiagnosis.absentSymptoms.length,
    status: "negated",
    items: previewDiagnosis.absentSymptoms,
    tone: "red",
  },
];

const recommendationGroups = [
  {
    label: "Consult",
    items: previewDiagnosis.recommendation.specialistConsultations,
    tone: "blue",
  },
  {
    label: "Test",
    items: previewDiagnosis.recommendation.labTests,
    tone: "green",
  },
];

function FindingIcon({ type }: { type: string }) {
  if (type === "check") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M20 6 9 17l-5-5" />
      </svg>
    );
  }

  if (type === "minus") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M5 12h14" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="7" />
      <circle cx="12" cy="12" r="2" />
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
    </svg>
  );
}

type ReasoningAccordionItemProps = {
  defaultOpen?: boolean;
  label: string;
  reason: string;
  status: string;
};

function ReasoningAccordionItem({
  defaultOpen = false,
  label,
  reason,
  status,
}: ReasoningAccordionItemProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <article className={isOpen ? "is-open" : ""}>
      <button
        aria-expanded={isOpen}
        className="reasoning-card-title"
        onClick={() => setIsOpen((current) => !current)}
        type="button"
      >
        <strong>{label}</strong>
        <span>{status}</span>
      </button>
      {isOpen ? <p>{reason}</p> : null}
    </article>
  );
}

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
              <strong className="input-badge">Input</strong>
            </div>
            <p>{previewDiagnosis.inputText}</p>
            <div className="preview-action-row" aria-hidden="true">
              <span>Run diagnosis</span>
              <span>Clear</span>
            </div>
          </article>

          <div className="finding-list">
            {findingCards.map((finding) => (
              <article
                className={`finding-card finding-card-${finding.tone}`}
                key={finding.label}
              >
                <div>
                  <div className="finding-heading">
                    <small>
                      <FindingIcon type={finding.icon} />
                      {finding.label}
                    </small>
                    <span aria-label={`${finding.label} count`}>
                      {finding.count} {finding.status}
                    </span>
                  </div>
                  <div className="finding-chips">
                    {finding.items.map((item) => (
                      <strong key={item}>{item}</strong>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>

        <div className="workspace-right">
          <article className="result-panel">
            <div className="result-summary">
              <div className="diagnosis-summary-card">
                <div className="result-title-row">
                  <span className="panel-kicker">Explainable result</span>
                  <strong>Top candidate</strong>
                </div>
                <h2>{previewDiagnosis.mostLikely}</h2>
                <p>{previewDiagnosis.primaryAnalysis}</p>
              </div>

              <div className="confidence-card">
                <div className="confidence-card-header">
                  <span>Confidence</span>
                  <strong>{previewDiagnosis.confidence}</strong>
                </div>
                <div className="progress-track" aria-hidden="true">
                  <span />
                </div>
                <small>Symptom match</small>
              </div>
            </div>

            <div className="result-content-grid">
              <div className="result-column">
                <div className="reasoning-list">
                  <div className="section-heading">
                    <span>Differential comparison</span>
                  </div>
                  {previewDiagnosis.differentialComparison.map((item, index) => (
                    <ReasoningAccordionItem
                      defaultOpen={index === 0}
                      key={item.disease}
                      label={item.disease}
                      reason={item.reasoning}
                      status="Alternative"
                    />
                  ))}
                </div>

                <div className="reasoning-list compact ruled-out-panel">
                  <div className="section-heading">
                    <span>Ruled out</span>
                  </div>
                  {previewDiagnosis.exclusionCriteria.map((item) => (
                    <ReasoningAccordionItem
                      key={item.disease}
                      label={item.disease}
                      reason={item.reasoning}
                      status="Negated"
                    />
                  ))}
                </div>
              </div>

              <div className="result-column result-column-care">
                <div className="recommendation-groups">
                  {recommendationGroups.map((group) => (
                    <section
                      className={`recommendation-group recommendation-group-${group.tone}`}
                      key={group.label}
                    >
                      <div className="section-heading recommendation-heading">
                        <span>{group.label}</span>
                      </div>
                      <div className="recommendation-chips">
                        {group.items.map((item) => (
                          <strong key={item}>{item}</strong>
                        ))}
                      </div>
                    </section>
                  ))}
                  <section className="recommendation-group recommendation-group-amber verify-strip">
                    <div className="section-heading recommendation-heading">
                      <span>Verify</span>
                    </div>
                    <div className="recommendation-chips monitor-chips">
                      {previewDiagnosis.recommendation.symptomsToVerify.map(
                        (item) => (
                          <strong key={item}>{item}</strong>
                        ),
                      )}
                    </div>
                  </section>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  );
}

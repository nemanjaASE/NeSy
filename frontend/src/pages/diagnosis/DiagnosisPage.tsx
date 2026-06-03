import { useMemo, useState } from "react";
import type { FormEvent } from "react";
import { runDiagnosis } from "@/features/diagnostics/api";
import type { DiagnosticResponse } from "@/features/diagnostics/types";
import { AppShell } from "@/shared/ui/AppShell";
import { WindowControls } from "@/shared/ui/WindowControls/WindowControls";
import { SiteFooter } from "@/pages/home/ui/SiteFooter";
import { SiteHeader } from "@/pages/home/ui/SiteHeader";
import "../home/HomePage.css";
import "./DiagnosisPage.css";

const initialNarrative =
  "I've been feeling very tired and nauseous for the past few days. My skin and eyes have turned yellow, and I noticed my stool has become pale and my urine is very dark. I do not feel drowsy and I am not confused.";

type ReasoningAccordionItemProps = {
  defaultOpen?: boolean;
  label: string;
  reason: string;
  status: string;
};

function FindingIcon({ type }: { type: "check" | "minus" }) {
  if (type === "check") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M20 6 9 17l-5-5" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 12h14" />
    </svg>
  );
}

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

function EmptyResult() {
  return (
    <article className="diagnosis-empty-state">
      <span>Awaiting input</span>
      <h2>Run a diagnosis to generate an explainable result.</h2>
      <p>
        The response will show extracted symptoms, ranked candidates,
        differential reasoning, exclusions, and recommended next steps.
      </p>
    </article>
  );
}

export function DiagnosisPage() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [narrative, setNarrative] = useState(initialNarrative);
  const [result, setResult] = useState<DiagnosticResponse | null>(null);

  const findingCards = useMemo(() => {
    const present = result?.present_symptoms ?? [];
    const absent = result?.absent_symptoms ?? [];

    return [
      {
        count: present.length,
        icon: "check" as const,
        items: present,
        label: "Present",
        status: "detected",
        tone: "green",
      },
      {
        count: absent.length,
        icon: "minus" as const,
        items: absent,
        label: "Absent",
        status: "negated",
        tone: "red",
      },
    ];
  }, [result]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const text = narrative.trim();
    if (!text) {
      setError("Patient narrative is required.");
      return;
    }

    setError(null);
    setIsLoading(true);

    try {
      const response = await runDiagnosis({ text });
      setResult(response);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to run diagnosis.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  const explanation = result?.explanation;

  return (
    <AppShell>
      <SiteHeader />

      <section className="diagnosis-page">
        <div className="diagnosis-hero">
          <span>Start diagnosis</span>
          <h1>Run an explainable diagnostic pass.</h1>
          <p>
            Enter a patient narrative, send it to the FastAPI backend, and
            inspect the structured neuro-symbolic result.
          </p>
        </div>

        <section className="workspace diagnosis-workspace">
          <div className="workspace-header">
            <WindowControls />
            <p>diagnosis.workspace</p>
          </div>

          <div className="workspace-grid">
            <div className="workspace-left">
              <form
                aria-busy={isLoading}
                className={`diagnosis-input-panel${isLoading ? " is-loading" : ""}`}
                onSubmit={handleSubmit}
              >
                <div className="panel-heading">
                  <span>Patient narrative</span>
                  <strong className="input-badge">Input</strong>
                </div>

                <textarea
                  aria-label="Patient narrative"
                  disabled={isLoading}
                  onChange={(event) => setNarrative(event.target.value)}
                  placeholder="Describe the patient's symptoms, including what they deny..."
                  value={narrative}
                />

                <div className="diagnosis-actions">
                  <button disabled={isLoading} type="submit">
                    {isLoading ? (
                      <>
                        <span className="diagnosis-spinner" aria-hidden="true" />
                        Running diagnosis
                      </>
                    ) : (
                      "Run diagnosis"
                    )}
                  </button>
                  <button
                    disabled={isLoading}
                    onClick={() => {
                      setError(null);
                      setNarrative("");
                      setResult(null);
                    }}
                    type="button"
                  >
                    Clear
                  </button>
                </div>

                {error ? <p className="diagnosis-error">{error}</p> : null}
              </form>

              {result ? (
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
              ) : null}
            </div>

            <div className="workspace-right">
              <article className="result-panel diagnosis-result-panel">
                {!explanation ? (
                  <EmptyResult />
                ) : (
                  <>
                    <div className="result-summary">
                      <div className="diagnosis-summary-card">
                        <div className="result-title-row">
                          <span className="panel-kicker">
                            Explainable result
                          </span>
                          <strong>Top candidate</strong>
                        </div>
                        <h2>{explanation.most_likely}</h2>
                        <p>{explanation.reasoning.primary_analysis}</p>
                      </div>

                      <div className="confidence-card">
                        <div className="confidence-card-header">
                          <span>Confidence</span>
                          <strong>{explanation.confidence}</strong>
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
                          {explanation.reasoning.differential_comparison.map(
                            (item, index) => (
                              <ReasoningAccordionItem
                                defaultOpen={index === 0}
                                key={item.disease}
                                label={item.disease}
                                reason={item.reasoning}
                                status="Alternative"
                              />
                            ),
                          )}
                        </div>

                        <div className="reasoning-list compact ruled-out-panel">
                          <div className="section-heading">
                            <span>Ruled out</span>
                          </div>
                          {explanation.reasoning.exclusion_criteria.map(
                            (item) => (
                              <ReasoningAccordionItem
                                key={item.excluded_disease}
                                label={item.excluded_disease}
                                reason={item.reasoning}
                                status="Negated"
                              />
                            ),
                          )}
                        </div>
                      </div>

                      <div className="result-column result-column-care">
                        <div className="recommendation-groups">
                          <section className="recommendation-group recommendation-group-blue">
                            <div className="section-heading recommendation-heading">
                              <span>Consult</span>
                            </div>
                            <div className="recommendation-chips">
                              {explanation.recommendation.specialist_consultations.map(
                                (item) => (
                                  <strong key={item}>{item}</strong>
                                ),
                              )}
                            </div>
                          </section>

                          <section className="recommendation-group recommendation-group-green">
                            <div className="section-heading recommendation-heading">
                              <span>Test</span>
                            </div>
                            <div className="recommendation-chips">
                              {explanation.recommendation.lab_tests.map(
                                (item) => (
                                  <strong key={item}>{item}</strong>
                                ),
                              )}
                            </div>
                          </section>

                          <section className="recommendation-group recommendation-group-amber verify-strip">
                            <div className="section-heading recommendation-heading">
                              <span>Verify</span>
                            </div>
                            <div className="recommendation-chips monitor-chips">
                              {explanation.recommendation.symptoms_to_verify.map(
                                (item) => (
                                  <strong key={item}>{item}</strong>
                                ),
                              )}
                            </div>
                          </section>
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </article>
            </div>
          </div>
        </section>
      </section>

      <SiteFooter />
    </AppShell>
  );
}

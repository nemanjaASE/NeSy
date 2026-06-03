import { useEffect, useState } from "react";
import { previewDiagnosis } from "../model/content";
import { KnowledgeGraphVisual } from "./KnowledgeGraphVisual";

const slides = [
  {
    eyebrow: "Knowledge graph",
    title: "Disease-symptom links",
    visual: "graph",
  },
  {
    eyebrow: "Reasoning path",
    title: "From narrative to explanation",
    visual: "path",
  },
  {
    eyebrow: "Clinical output",
    title: "Hepatitis E result preview",
    visual: "output",
  },
];

const reasoningSteps = [
  {
    icon: "text",
    label: "Extract",
    text: "present and absent symptoms",
  },
  {
    icon: "link",
    label: "Map",
    text: "phrases to ontology terms",
  },
  {
    icon: "graph",
    label: "Infer",
    text: "diseases through Neo4j",
  },
  {
    icon: "score",
    label: "Score",
    text: "rank and filter candidates",
  },
  {
    icon: "spark",
    label: "Explain",
    text: "ranked reasoning output",
  },
];

function StepIcon({ type }: { type: string }) {
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
        <path d="M5 19V9" />
        <path d="M12 19V5" />
        <path d="M19 19v-7" />
        <path d="M4 19h16" />
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

function ReasoningPathVisual() {
  return (
    <div className="reasoning-path-visual" aria-hidden="true">
      <div className="symbol-flow">
        {reasoningSteps.map((step) => (
          <div className="symbol-step" key={step.label}>
            <div className="symbol-icon">
              <StepIcon type={step.icon} />
            </div>
            <strong>{step.label}</strong>
            <span>{step.text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function ClinicalOutputVisual() {
  return (
    <div className="clinical-output-visual" aria-hidden="true">
      <div className="mini-result-window">
        <div className="mini-result-bar">
          <span />
          <span />
          <span />
        </div>

        <div className="mini-preview-body">
          <div className="mini-preview-left">
            <section className="mini-code-panel">
              <div className="mini-panel-heading">
                <span>Patient narrative</span>
                <strong>Input</strong>
              </div>
              <p>{previewDiagnosis.inputText}</p>
            </section>

            <section className="mini-finding-card mini-finding-card-green">
              <div className="mini-panel-heading">
                <span>Present</span>
                <strong>{previewDiagnosis.presentSymptoms.length} detected</strong>
              </div>
              <div className="mini-token-grid">
                {previewDiagnosis.presentSymptoms.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </div>
            </section>

            <section className="mini-finding-card mini-finding-card-red">
              <div className="mini-panel-heading">
                <span>Absent</span>
                <strong>{previewDiagnosis.absentSymptoms.length} negated</strong>
              </div>
              <div className="mini-token-grid">
                {previewDiagnosis.absentSymptoms.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </div>
            </section>
          </div>

          <div className="mini-preview-right">
            <div className="mini-result-grid">
              <section className="mini-diagnosis-card">
                <span>Top candidate</span>
                <strong>{previewDiagnosis.mostLikely}</strong>
                <p>{previewDiagnosis.primaryAnalysis}</p>
              </section>

              <section className="mini-side-card">
                <div className="output-meter">
                  <span>Confidence</span>
                  <strong>{previewDiagnosis.confidence}</strong>
                  <div>
                    <i />
                  </div>
                  <small>Symptom match</small>
                </div>
              </section>
            </div>

            <section className="mini-reasoning-panel">
              <small>Differential comparison</small>
              <div className="mini-reasoning-row">
                {previewDiagnosis.differentialComparison
                  .slice(0, 2)
                  .map((item) => (
                    <article key={item.disease}>
                      <strong>{item.disease}</strong>
                      <span>Alternative</span>
                    </article>
                  ))}
              </div>
            </section>

            <div className="mini-bottom-grid">
              <article>
                <small>Ruled out</small>
                <strong>{previewDiagnosis.exclusionCriteria[0]?.disease}</strong>
              </article>
              <article>
                <small>Consult</small>
                <div className="mini-care-chips">
                  {previewDiagnosis.recommendation.specialistConsultations.map(
                    (item) => (
                      <span key={item}>{item}</span>
                    ),
                  )}
                </div>
              </article>
              <article>
                <small>Test</small>
                <div className="mini-care-chips">
                  {previewDiagnosis.recommendation.labTests
                    .slice(0, 2)
                    .map((item) => (
                      <span key={item}>{item}</span>
                    ))}
                </div>
              </article>
              <article>
                <small>Verify</small>
                <div className="mini-care-chips">
                  {previewDiagnosis.recommendation.symptomsToVerify
                    .slice(0, 2)
                    .map((item) => (
                      <span key={item}>{item}</span>
                    ))}
                </div>
              </article>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function HeroVisualCarousel() {
  const [activeSlide, setActiveSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    if (isPaused) {
      return;
    }

    const intervalId = window.setInterval(() => {
      setActiveSlide((current) => (current + 1) % slides.length);
    }, 4500);

    return () => window.clearInterval(intervalId);
  }, [isPaused]);

  return (
    <aside
      className="hero-visual-carousel"
      aria-label="Diagnostic workflow preview"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      <div className="carousel-stage">
        {slides.map((slide, index) => (
          <section
            className={`carousel-slide${index === activeSlide ? " is-active" : ""}`}
            aria-hidden={index !== activeSlide}
            key={slide.title}
          >
            <div className="carousel-caption">
              <span>{slide.eyebrow}</span>
              <strong>{slide.title}</strong>
            </div>

            {slide.visual === "graph" ? <KnowledgeGraphVisual /> : null}
            {slide.visual === "path" ? <ReasoningPathVisual /> : null}
            {slide.visual === "output" ? <ClinicalOutputVisual /> : null}
          </section>
        ))}
      </div>

      <div className="carousel-dots" aria-label="Select preview slide">
        {slides.map((slide, index) => (
          <button
            aria-label={`Show ${slide.eyebrow}`}
            aria-pressed={index === activeSlide}
            className={index === activeSlide ? "is-active" : ""}
            key={slide.title}
            onClick={() => setActiveSlide(index)}
            type="button"
          />
        ))}
      </div>
    </aside>
  );
}

import { AppShell } from "@/shared/ui/AppShell";
import { SiteFooter } from "@/pages/home/ui/SiteFooter";
import { SiteHeader } from "@/pages/home/ui/SiteHeader";
import "../home/HomePage.css";
import "./ModelsPage.css";
import { useEffect, useState, type CSSProperties } from "react";
import {
  embeddingModelProfiles,
  evaluatedEmbeddingModels,
  evaluatedExtractionModels,
  evaluatedXaiModels,
  llmModelProfiles,
  selectedModelStack,
} from "./model/content";

type ScoreStyle = CSSProperties & {
  "--score-width": string;
};

type ActiveBenchmark = "nlp" | "embedding" | "xai";

export function ModelsPage() {
  const [activeBenchmark, setActiveBenchmark] = useState<ActiveBenchmark>("nlp");
  const [activeEmbeddingModel, setActiveEmbeddingModel] = useState(0);
  const [activeModel, setActiveModel] = useState(0);
  const [isEmbeddingCarouselPaused, setIsEmbeddingCarouselPaused] =
    useState(false);
  const [isModelCarouselPaused, setIsModelCarouselPaused] = useState(false);

  const benchmarkTitle = {
    embedding: "Embedding benchmark",
    nlp: "NLP extraction benchmark",
    xai: "XAI benchmark",
  }[activeBenchmark];

  const benchmarkBadges = {
    embedding: ["369 mappings", "3 models"],
    nlp: ["100 cases", "7 models"],
    xai: ["4 scenarios", "7 models"],
  }[activeBenchmark];

  const metricGuide = {
    embedding: [
      ["Usable", "Mappings with confidence high enough for downstream use."],
      ["Confidence", "Average cosine similarity between input and ontology terms."],
      ["Bad match", "Mappings below the accepted confidence threshold."],
      ["SYN", "Performance on synonyms and colloquial symptom expressions."],
      ["LLM", "Performance on symptoms extracted by the NLP layer."],
    ],
    nlp: [
      ["Precision", "How many extracted symptoms were relevant and correct."],
      ["Recall", "How many expected symptoms were found in the narrative."],
      ["F1 score", "Balanced score combining precision and recall."],
    ],
    xai: [
      ["JSON", "Whether the model followed the required response schema."],
      ["Exclusion", "Correct handling of blocked diseases and denied symptoms."],
      ["Consistency", "Whether reasoning text supports the structured result."],
      ["Tone", "Clinical clarity and appropriate medical vocabulary."],
      ["Time", "Total generation time across the XAI test scenarios."],
    ],
  }[activeBenchmark];

  const currentModel = llmModelProfiles[activeModel];
  const currentEmbeddingModel = embeddingModelProfiles[activeEmbeddingModel];

  useEffect(() => {
    if (isModelCarouselPaused) {
      return;
    }

    const intervalId = window.setInterval(() => {
      setActiveModel((current) => (current + 1) % llmModelProfiles.length);
    }, 5200);

    return () => window.clearInterval(intervalId);
  }, [isModelCarouselPaused]);

  useEffect(() => {
    if (isEmbeddingCarouselPaused) {
      return;
    }

    const intervalId = window.setInterval(() => {
      setActiveEmbeddingModel(
        (current) => (current + 1) % embeddingModelProfiles.length,
      );
    }, 5800);

    return () => window.clearInterval(intervalId);
  }, [isEmbeddingCarouselPaused]);

  return (
    <AppShell>
      <SiteHeader />

      <section className="models-page">
        <div className="models-hero">
          <span>Model stack</span>
          <h1>LLMs constrained by graph reasoning.</h1>
          <p>
            NeSy uses language models where they are strongest: extraction and
            explanation. Ontology mapping, disease search, filtering, and
            ranking remain grounded in the symbolic graph.
          </p>
        </div>

        <section className="model-stack-grid" aria-label="Selected model stack">
          {selectedModelStack.map((model) => (
            <article
              className={`model-card model-card-${model.accent}`}
              key={`${model.role}-${model.name}`}
            >
              <div className="model-card-header">
                <span>{model.tag}</span>
                <strong>{model.role}</strong>
              </div>
              <div className="selected-model-badge">
                {model.selectedLabel}
              </div>
              <h2>{model.name}</h2>
              <p>{model.summary}</p>

              <div className="model-metrics">
                {model.metrics.map((metric) => (
                  <div key={metric.label}>
                    <strong>{metric.value}</strong>
                    <span>{metric.label}</span>
                  </div>
                ))}
              </div>

              <div className="model-rationale">
                <span>Why this model</span>
                <p>{model.why}</p>
              </div>
            </article>
          ))}
        </section>

        <section className="models-analysis-grid">
          <div className="model-profile-column">
            <article
              className="models-panel llm-profile-carousel"
              onFocus={() => setIsModelCarouselPaused(true)}
              onMouseEnter={() => setIsModelCarouselPaused(true)}
              onMouseLeave={() => setIsModelCarouselPaused(false)}
            >
              <div className="models-panel-heading">
                <span>LLM model profiles</span>
                <strong>{currentModel.type}</strong>
              </div>

              <div className="llm-profile-card">
                <div className="llm-profile-topline">
                  <span>{String(activeModel + 1).padStart(2, "0")}</span>
                  {currentModel.winner ? (
                    <strong>Top extraction model</strong>
                  ) : null}
                </div>

                <h2>{currentModel.model}</h2>
                <p>{currentModel.commentary}</p>

                <div className="llm-profile-metrics">
                  <div>
                    <span>Developer</span>
                    <strong>{currentModel.developer}</strong>
                  </div>
                  <div>
                    <span>Parameters</span>
                    <strong>{currentModel.parameters}</strong>
                  </div>
                  <div>
                    <span>Context</span>
                    <strong>{currentModel.context}</strong>
                  </div>
                  <div>
                    <span>F1 score</span>
                    <strong>{currentModel.f1}</strong>
                  </div>
                  <div>
                    <span>Speed</span>
                    <strong>{currentModel.performance}</strong>
                  </div>
                  <div>
                    <span>Released</span>
                    <strong>{currentModel.release}</strong>
                  </div>
                </div>

                <div className="llm-architecture">
                  <span>Architecture</span>
                  <strong>{currentModel.architecture}</strong>
                </div>
              </div>

              <div className="llm-carousel-dots" aria-label="Select LLM profile">
                {llmModelProfiles.map((model, index) => (
                  <button
                    aria-label={`Show ${model.model}`}
                    aria-pressed={activeModel === index}
                    className={activeModel === index ? "is-active" : ""}
                    key={model.model}
                    onClick={() => setActiveModel(index)}
                    type="button"
                  />
                ))}
              </div>
            </article>

            <article
              className="models-panel llm-profile-carousel embedding-profile-carousel"
              onFocus={() => setIsEmbeddingCarouselPaused(true)}
              onMouseEnter={() => setIsEmbeddingCarouselPaused(true)}
              onMouseLeave={() => setIsEmbeddingCarouselPaused(false)}
            >
              <div className="models-panel-heading">
                <span>Embedding model profiles</span>
                <strong>{currentEmbeddingModel.type}</strong>
              </div>

              <div className="llm-profile-card embedding-profile-card">
                <div className="llm-profile-topline">
                  <span>
                    {String(activeEmbeddingModel + 1).padStart(2, "0")}
                  </span>
                  {currentEmbeddingModel.winner ? (
                    <strong>Selected embedding model</strong>
                  ) : null}
                </div>

                <h2>{currentEmbeddingModel.model}</h2>
                <p>{currentEmbeddingModel.commentary}</p>

                <div className="llm-profile-metrics">
                  <div>
                    <span>Dimensions</span>
                    <strong>{currentEmbeddingModel.dimensions}</strong>
                  </div>
                  <div>
                    <span>Use case</span>
                    <strong>{currentEmbeddingModel.useCase}</strong>
                  </div>
                  <div>
                    <span>Exact match</span>
                    <strong>{currentEmbeddingModel.exactMatch}</strong>
                  </div>
                  <div>
                    <span>Usable</span>
                    <strong>{currentEmbeddingModel.usableMatchRate}</strong>
                  </div>
                  <div>
                    <span>Confidence</span>
                    <strong>{currentEmbeddingModel.averageConfidence}</strong>
                  </div>
                  <div>
                    <span>Bad match</span>
                    <strong>{currentEmbeddingModel.badMatchRate}</strong>
                  </div>
                </div>
              </div>

              <div
                className="llm-carousel-dots"
                aria-label="Select embedding profile"
              >
                {embeddingModelProfiles.map((model, index) => (
                  <button
                    aria-label={`Show ${model.model}`}
                    aria-pressed={activeEmbeddingModel === index}
                    className={
                      activeEmbeddingModel === index ? "is-active" : ""
                    }
                    key={model.model}
                    onClick={() => setActiveEmbeddingModel(index)}
                    type="button"
                  />
                ))}
              </div>
            </article>
          </div>

          <article className="models-panel models-leaderboard benchmark-carousel">
            <div className="models-panel-heading benchmark-carousel-heading">
              <div>
                <span>{benchmarkTitle}</span>
                <div className="benchmark-count-badges">
                  {benchmarkBadges.map((badge, index) => (
                    <strong
                      className={`benchmark-count-badge-${index + 1}`}
                      key={badge}
                    >
                      {badge}
                    </strong>
                  ))}
                </div>
              </div>

              <div className="benchmark-switch" aria-label="Select benchmark">
                <button
                  className={activeBenchmark === "nlp" ? "is-active" : ""}
                  onClick={() => setActiveBenchmark("nlp")}
                  type="button"
                >
                  NLP
                </button>
                <button
                  className={activeBenchmark === "embedding" ? "is-active" : ""}
                  onClick={() => setActiveBenchmark("embedding")}
                  type="button"
                >
                  Embedding
                </button>
                <button
                  className={activeBenchmark === "xai" ? "is-active" : ""}
                  onClick={() => setActiveBenchmark("xai")}
                  type="button"
                >
                  XAI
                </button>
              </div>
            </div>

            <p className="benchmark-environment-note">
              Results are measured on the documented local test setup and may
              vary across hardware, runtime, quantization, prompts, and
              providers.
            </p>

            {activeBenchmark === "nlp" ? (
              <>
                <div className="leaderboard-list">
                  {evaluatedExtractionModels.map((model, index) => (
                    <div
                      className={model.winner ? "is-winner" : undefined}
                      key={model.model}
                    >
                      <span className="leaderboard-rank">
                        {String(index + 1).padStart(2, "0")}
                      </span>
                      <div className="leaderboard-model">
                        <strong>{model.model}</strong>
                        <small>{model.type}</small>
                      </div>
                      <div className="leaderboard-score">
                        <div
                          style={
                            {
                              "--score-width": `${Number(model.precision) * 100}%`,
                            } as ScoreStyle
                          }
                        >
                          <small>Precision</small>
                          <strong>{model.precision}</strong>
                          <span>
                            <i />
                          </span>
                        </div>
                        <div
                          style={
                            {
                              "--score-width": `${Number(model.recall) * 100}%`,
                            } as ScoreStyle
                          }
                        >
                          <small>Recall</small>
                          <strong>{model.recall}</strong>
                          <span>
                            <i />
                          </span>
                        </div>
                        <div
                          className="is-primary-metric"
                          style={
                            {
                              "--score-width": `${Number(model.f1) * 100}%`,
                            } as ScoreStyle
                          }
                        >
                          <small>F1 score</small>
                          <strong>{model.f1}</strong>
                          <span>
                            <i />
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : activeBenchmark === "embedding" ? (
              <div className="compact-benchmark-list">
                {evaluatedEmbeddingModels.map((model, index) => (
                  <div
                    className={model.winner ? "is-winner" : undefined}
                    key={model.model}
                  >
                    <span className="benchmark-rank">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <div className="benchmark-model">
                      <strong>{model.model}</strong>
                      <small>Embedding model</small>
                    </div>
                    <dl>
                      <div>
                        <dt>Usable</dt>
                        <dd>{model.usableMatchRate}</dd>
                      </div>
                      <div>
                        <dt>Confidence</dt>
                        <dd>{model.averageConfidence}</dd>
                      </div>
                      <div>
                        <dt>Bad match</dt>
                        <dd>{model.badMatchRate}</dd>
                      </div>
                      <div>
                        <dt>SYN</dt>
                        <dd>{model.synonymMatch}</dd>
                      </div>
                      <div>
                        <dt>LLM</dt>
                        <dd>{model.llmMatch}</dd>
                      </div>
                    </dl>
                  </div>
                ))}
              </div>
            ) : (
              <div className="compact-benchmark-list xai-benchmark-list">
                {evaluatedXaiModels.map((model, index) => (
                  <div
                    className={model.winner ? "is-winner" : undefined}
                    key={model.model}
                  >
                    <span className="benchmark-rank">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <div className="benchmark-model">
                      <strong>{model.model}</strong>
                      <small>XAI model</small>
                    </div>
                    <dl>
                      <div>
                        <dt>JSON</dt>
                        <dd>{model.jsonIntegrity}</dd>
                      </div>
                      <div>
                        <dt>Exclusion</dt>
                        <dd>{model.exclusionLogic}</dd>
                      </div>
                      <div>
                        <dt>Consistency</dt>
                        <dd>{model.consistency}</dd>
                      </div>
                      <div>
                        <dt>Tone</dt>
                        <dd>{model.clinicalTone}</dd>
                      </div>
                      <div>
                        <dt>Time</dt>
                        <dd>{model.totalTime}</dd>
                      </div>
                    </dl>
                  </div>
                ))}
              </div>
            )}

            <div className="benchmark-metric-guide">
              {metricGuide.map(([label, description]) => (
                <p key={label}>
                  <strong>{label}</strong>
                  {description}
                </p>
              ))}
            </div>
          </article>
        </section>
      </section>

      <SiteFooter />
    </AppShell>
  );
}

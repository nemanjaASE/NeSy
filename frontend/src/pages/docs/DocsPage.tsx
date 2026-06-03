import { AppShell } from "@/shared/ui/AppShell";
import { SiteFooter } from "@/pages/home/ui/SiteFooter";
import { SiteHeader } from "@/pages/home/ui/SiteHeader";
import "../home/HomePage.css";
import "./DocsPage.css";
import {
  apiRequestExample,
  apiResponseFields,
  benchmarkNotes,
  docsNavItems,
  envVariables,
  githubReferences,
  inferenceBenchmarkNotes,
  limitationNotes,
  ontologyNotes,
  setupNotes,
} from "./model/content";

function GitReference({ href }: { href: string }) {
  return (
    <a className="git-reference" href={href} rel="noreferrer" target="_blank">
      GitHub reference
    </a>
  );
}

export function DocsPage() {
  return (
    <AppShell>
      <SiteHeader />

      <section className="docs-page">
        <div className="docs-hero">
          <span>Documentation</span>
          <h1>Technical documentation</h1>
          <p>
            Reference notes for the API contract, response schema, model
            configuration, benchmarks, and known limitations.
          </p>
          <GitReference href={githubReferences.repository} />
        </div>

        <div className="docs-layout">
          <aside className="docs-sidebar" aria-label="Documentation sections">
            <span>Contents</span>
            {docsNavItems.map((item) => (
              <a href={item.href} key={item.href}>
                {item.label}
              </a>
            ))}
          </aside>

          <div className="docs-content">
            <section className="docs-section" id="overview">
              <span>Overview</span>
              <h2>From patient narrative to explainable result.</h2>
              <p>
                NeSy combines neural language models with symbolic graph
                reasoning. The runtime flow extracts symptoms, maps them to
                ontology concepts, searches the Neo4j disease graph, ranks
                candidates, and returns an explanation with recommended next
                steps.
              </p>
              <div className="docs-flow">
                {["Extract", "Embed", "Infer", "Score", "Explain"].map(
                  (step) => (
                    <strong key={step}>{step}</strong>
                  ),
                )}
              </div>
            </section>

            <section className="docs-section" id="ontologies">
              <span>Ontologies</span>
              <h2>Grounding comes from DOID, SYMP, and has_symptom relations.</h2>
              <p>
                The symbolic layer is built around biomedical ontologies. DOID
                provides disease concepts, SYMP provides symptom concepts, and
                RO_0002452 defines the formal has_symptom relation used for graph
                traversal.
              </p>
              <div className="schema-grid">
                {ontologyNotes.map((item) => (
                  <article key={item.label}>
                    <strong>{item.label}</strong>
                    <p>{item.text}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="docs-section" id="scoring">
              <span>Scoring</span>
              <h2>Ranking favors specific symptoms over generic volume.</h2>
              <p>
                Disease ranking uses Information Content weights and square-root
                normalization so a disease with fewer high-specificity symptoms
                can outrank a broad disease with many generic symptoms.
              </p>
              <pre>
                <code>
                  normalized_score = sum(IC matched symptoms) / sqrt(count
                  disease symptoms)
                </code>
              </pre>
            </section>

            <section className="docs-section" id="api">
              <span>API usage</span>
              <h2>Send a patient narrative to the backend.</h2>
              <p>
                The frontend sends free-form clinical text to FastAPI. The
                backend returns structured symptoms, ranked disease candidates,
                reasoning, exclusions, and follow-up recommendations.
              </p>
              <pre>
                <code>{apiRequestExample}</code>
              </pre>
            </section>

            <section className="docs-section" id="schema">
              <span>Response schema</span>
              <h2>Use the payload as structured UI state.</h2>
              <div className="schema-grid">
                {apiResponseFields.map((item) => (
                  <article key={item.field}>
                    <strong>{item.field}</strong>
                    <p>{item.text}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="docs-section" id="configuration">
              <span>Configuration</span>
              <h2>Model and API settings live in environment variables.</h2>
              <div className="env-list">
                {envVariables.map((item) => (
                  <article key={item.name}>
                    <code>{item.name}</code>
                    <p>{item.text}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="docs-section" id="benchmarks">
              <span>Benchmarks</span>
              <h2>Interpret scores in the documented test environment.</h2>
              <div className="docs-note-list">
                {benchmarkNotes.map((note) => (
                  <p key={note}>{note}</p>
                ))}
              </div>
            </section>

            <section className="docs-section" id="inference">
              <span>Inference benchmark</span>
              <h2>Symbolic graph ranking was tested independently.</h2>
              <p>
                The inference layer queries Neo4j using mapped symptoms, ranks
                candidate diseases, and validates deterministic exclusion for
                absent symptoms.
              </p>
              <div className="schema-grid">
                {inferenceBenchmarkNotes.map((item) => (
                  <article key={item.label}>
                    <strong>{item.label}</strong>
                    <p>{item.text}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="docs-section" id="setup">
              <span>Setup notes</span>
              <h2>The graph must be prepared before runtime diagnosis.</h2>
              <div className="docs-note-list">
                {setupNotes.map((note) => (
                  <p key={note}>{note}</p>
                ))}
              </div>
            </section>

            <section className="docs-section warning-section" id="limitations">
              <span>Limitations</span>
              <h2>Research prototype, not a clinical decision-maker.</h2>
              <div className="docs-note-list">
                {limitationNotes.map((note) => (
                  <p key={note}>{note}</p>
                ))}
              </div>
            </section>
          </div>
        </div>
      </section>

      <SiteFooter />
    </AppShell>
  );
}

export const docsNavItems = [
  { href: "#overview", label: "Overview" },
  { href: "#ontologies", label: "Ontologies" },
  { href: "#scoring", label: "Scoring" },
  { href: "#api", label: "API usage" },
  { href: "#schema", label: "Response schema" },
  { href: "#configuration", label: "Configuration" },
  { href: "#benchmarks", label: "Benchmarks" },
  { href: "#inference", label: "Inference benchmark" },
  { href: "#setup", label: "Setup notes" },
  { href: "#limitations", label: "Limitations" },
];

export const githubReferences = {
  repository: "https://github.com/nemanjaASE/NeSy",
};

export const apiRequestExample = `{
  "input_text": "I've been feeling very tired and nauseous..."
}`;

export const apiResponseFields = [
  {
    field: "input_text",
    text: "Original patient narrative submitted by the user.",
  },
  {
    field: "present_symptoms",
    text: "Symptoms detected as explicitly present in the narrative.",
  },
  {
    field: "absent_symptoms",
    text: "Symptoms the patient explicitly denied.",
  },
  {
    field: "most_likely",
    text: "Highest ranked disease candidate after graph inference and scoring.",
  },
  {
    field: "differential_comparison",
    text: "Alternative candidates with natural-language reasoning.",
  },
  {
    field: "exclusion_criteria",
    text: "Conditions filtered out by absent or blocking symptoms.",
  },
  {
    field: "recommendation",
    text: "Suggested consultations, tests, and symptoms to verify.",
  },
];

export const envVariables = [
  {
    name: "LLM_EXTRACTION_MODEL_NAME",
    text: "Model used to extract present and absent symptoms from free text.",
  },
  {
    name: "LLM_XAI_MODEL_NAME",
    text: "Model used to generate transparent explanations from structured graph results.",
  },
  {
    name: "EMBEDDING_MODEL_NAME",
    text: "Sentence-transformer model used for symptom vectorization and ontology mapping.",
  },
  {
    name: "VITE_API_BASE_URL",
    text: "Frontend base URL for requests to the FastAPI backend.",
  },
];

export const benchmarkNotes = [
  "NLP extraction was evaluated across 100 clinical cases and 7 LLMs.",
  "Embedding mapping was evaluated across 369 symptom mappings and 3 sentence-transformer models.",
  "XAI was evaluated across 4 clinical scenarios designed to test exclusion logic, consistency, and clinical tone.",
];

export const ontologyNotes = [
  {
    label: "DOID",
    text: "Human Disease Ontology provides standardized disease concepts and hierarchy.",
  },
  {
    label: "SYMP",
    text: "Symptom Ontology provides normalized clinical signs and symptoms.",
  },
  {
    label: "RO_0002452",
    text: "Formal has_symptom relation connecting disease concepts to symptom concepts.",
  },
  {
    label: "n10s",
    text: "Neo4j neosemantics translates OWL/RDF restrictions into queryable graph structures.",
  },
];

export const inferenceBenchmarkNotes = [
  {
    label: "Full match",
    text: "Hit@1 85.4%, Hit@3 92.0%, Hit@5 93.2% across 424 diseases.",
  },
  {
    label: "Partial match drop=1",
    text: "Hit@1 57.3%, Hit@3 67.7%, Hit@5 71.2% with expected no-result cases.",
  },
  {
    label: "Partial match drop=2",
    text: "Hit@1 50.0%, Hit@3 63.0%, Hit@5 67.9% after filtering sparse diseases.",
  },
  {
    label: "Exclusion test",
    text: "100% exclusion accuracy and 100% survival accuracy across 1,263 cases.",
  },
];

export const setupNotes = [
  "Prepare Neo4j and load DOID/SYMP ontologies before running diagnosis.",
  "Run notebooks to calculate Information Content weights and generate symptom embeddings.",
  "Start the FastAPI backend after the graph has been enriched.",
  "Use Ollama or a cloud provider for LLM extraction and XAI generation.",
];

export const limitationNotes = [
  "NeSy is a research prototype and is not intended for clinical diagnosis.",
  "Disease coverage depends on the loaded DOID and SYMP ontology versions.",
  "Model outputs should be reviewed by a qualified medical professional.",
  "Benchmark results may vary across hardware, runtime, quantization, prompts, and API providers.",
];

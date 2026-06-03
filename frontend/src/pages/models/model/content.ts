export const selectedModelStack = [
  {
    accent: "cyan",
    metrics: [
      { label: "Precision", value: "0.835" },
      { label: "Recall", value: "0.825" },
      { label: "F1 score", value: "0.825" },
    ],
    name: "qwen2.5:14b",
    selectedLabel: "Selected extractor",
    role: "NLP extraction",
    summary:
      "Parses patient narratives into structured present and absent symptoms before the graph layer runs.",
    tag: "Extraction model",
    why:
      "Best extraction result in the documented 100-case evaluation, with strong structured output and perfect negation handling in the selected prompt setup.",
  },
  {
    accent: "violet",
    metrics: [
      { label: "Dimensions", value: "1024" },
      { label: "Usable", value: "94.0%" },
      { label: "Bad match", value: "6.0%" },
    ],
    name: "intfloat/multilingual-e5-large",
    selectedLabel: "Selected mapper",
    role: "Symptom embedding",
    summary:
      "Maps extracted symptom phrases to ontology symptoms through semantic similarity search.",
    tag: "Embedding model",
    why:
      "Selected after outperforming MiniLM and PubMedBERT on colloquial, exact, and LLM-extracted symptom mappings.",
  },
  {
    accent: "emerald",
    metrics: [
      { label: "JSON", value: "100%" },
      { label: "Exclusion", value: "100%" },
      { label: "Consistency", value: "High" },
    ],
    name: "qwen2.5:14b",
    selectedLabel: "Selected explainer",
    role: "XAI explanation",
    summary:
      "Turns ranked graph results into differential comparisons, ruled-out conditions, confidence, and next steps.",
    tag: "Explanation model",
    why:
      "In XAI tests it kept the structured schema intact and correctly respected passed_filter logic across all four clinical scenarios.",
  },
];

export const evaluatedExtractionModels = [
  {
    f1: "0.825",
    model: "qwen2.5:14b",
    precision: "0.835",
    recall: "0.825",
    type: "Local",
    winner: true,
  },
  {
    f1: "0.800",
    model: "llama3:8b",
    precision: "0.809",
    recall: "0.806",
    type: "Local",
  },
  {
    f1: "0.790",
    model: "mistral-nemo:12b",
    precision: "0.784",
    recall: "0.810",
    type: "Local",
  },
  {
    f1: "0.772",
    model: "phi4:14b",
    precision: "0.771",
    recall: "0.783",
    type: "Local",
  },
  {
    f1: "0.769",
    model: "llama-4-scout-17b",
    precision: "0.749",
    recall: "0.806",
    type: "Cloud",
  },
  {
    f1: "0.731",
    model: "llama3.2:3b",
    precision: "0.747",
    recall: "0.730",
    type: "Local",
  },
  {
    f1: "0.689",
    model: "gpt-oss-120b",
    precision: "0.695",
    recall: "0.697",
    type: "Cloud",
  },
];

export const llmModelProfiles = [
  {
    architecture: "Dense decoder-only Transformer",
    commentary:
      "Lightweight baseline with balanced extraction, but less reliable on complex negation and ontology-aligned phrasing.",
    context: "128K",
    developer: "Meta",
    f1: "0.731",
    model: "llama3.2:3b",
    parameters: "3.21B",
    performance: "0.39s / case",
    release: "September 2024",
    type: "Local",
  },
  {
    architecture: "Dense decoder-only Transformer",
    commentary:
      "Reached the 80% F1 target and handled present versus absent symptoms reliably, with some semantic mapping misses.",
    context: "8K",
    developer: "Meta",
    f1: "0.800",
    model: "llama3:8b",
    parameters: "8.03B",
    performance: "0.57s / case",
    release: "April 2024",
    type: "Local",
  },
  {
    architecture: "Dense decoder-only Transformer",
    commentary:
      "Strong recall and long context, but often used overly technical synonyms or merged separate symptoms.",
    context: "128K",
    developer: "Mistral AI + NVIDIA",
    f1: "0.790",
    model: "mistral-nemo:12b",
    parameters: "12.2B",
    performance: "0.79s / case",
    release: "July 2024",
    type: "Local",
  },
  {
    architecture: "Dense decoder-only Transformer",
    commentary:
      "Top extraction performer with the best F1 score, strong structured output, and robust negation handling.",
    context: "128K",
    developer: "Alibaba Cloud",
    f1: "0.825",
    model: "qwen2.5:14b",
    parameters: "14.7B",
    performance: "0.95s / case",
    release: "September 2024",
    type: "Local",
    winner: true,
  },
  {
    architecture: "Dense decoder-only Transformer",
    commentary:
      "Clinically capable, but sometimes over-specified symptoms compared with the expected ontology-friendly labels.",
    context: "16K",
    developer: "Microsoft Research",
    f1: "0.772",
    model: "phi4:14b",
    parameters: "14B",
    performance: "1.16s / case",
    release: "December 2024",
    type: "Local",
  },
  {
    architecture: "Mixture-of-Experts autoregressive model",
    commentary:
      "Cloud MoE model with broad capability, but extraction suffered from clinically precise false positives.",
    context: "128K",
    developer: "Meta",
    f1: "0.769",
    model: "llama-4-scout-17b",
    parameters: "17B active / 109B total",
    performance: "2.07s / case",
    release: "April 2025",
    type: "Cloud",
  },
  {
    architecture: "Dense decoder-only Transformer",
    commentary:
      "Most descriptive model, but least label-compliant for this benchmark because it generated nuanced medical terms.",
    context: "Cloud API",
    developer: "OpenAI",
    f1: "0.689",
    model: "gpt-oss-120b",
    parameters: "~120B",
    performance: "3.63s / case",
    release: "Cloud",
    type: "Cloud",
  },
];

export const embeddingModelProfiles = [
  {
    averageConfidence: "0.915",
    badMatchRate: "27.1%",
    commentary:
      "Fast general-purpose baseline that works for exact labels, but struggles with informal symptom descriptions and clinical terminology.",
    dimensions: "384",
    exactMatch: "70.5%",
    model: "all-MiniLM-L6-v2",
    type: "General model",
    usableMatchRate: "72.9%",
    useCase: "General semantic similarity",
  },
  {
    averageConfidence: "0.917",
    badMatchRate: "27.6%",
    commentary:
      "Biomedical PubMed pretraining helps with formal clinical text, but it remains brittle on short colloquial patient phrases.",
    dimensions: "768",
    exactMatch: "70.5%",
    model: "NeuML/pubmedbert-base-embeddings",
    type: "Medical domain model",
    usableMatchRate: "72.4%",
    useCase: "Biomedical and scientific text",
  },
  {
    averageConfidence: "0.977",
    badMatchRate: "6.0%",
    commentary:
      "Selected embedding model. It handles ontology labels, clinical terms, and informal patient wording with the strongest usable match rate.",
    dimensions: "1024",
    exactMatch: "70.5%",
    model: "intfloat/multilingual-e5-large",
    type: "Multilingual large model",
    usableMatchRate: "94.0%",
    useCase: "Ontology alignment and mixed-register text",
    winner: true,
  },
];

export const evaluatedEmbeddingModels = [
  {
    averageConfidence: "0.977",
    badMatchRate: "6.0%",
    exactMatch: "1.000",
    llmMatch: "0.969",
    model: "intfloat/multilingual-e5-large",
    synonymMatch: "0.934",
    usableMatchRate: "94.0%",
    winner: true,
  },
  {
    averageConfidence: "0.917",
    badMatchRate: "27.6%",
    exactMatch: "1.000",
    llmMatch: "0.893",
    model: "NeuML/pubmedbert-base-embeddings",
    synonymMatch: "0.746",
    usableMatchRate: "72.4%",
  },
  {
    averageConfidence: "0.915",
    badMatchRate: "27.1%",
    exactMatch: "1.000",
    llmMatch: "0.879",
    model: "all-MiniLM-L6-v2",
    synonymMatch: "0.758",
    usableMatchRate: "72.9%",
  },
];

export const evaluatedXaiModels = [
  {
    clinicalTone: "High",
    consistency: "Fail",
    exclusionLogic: "25%",
    jsonIntegrity: "100%",
    model: "llama3.2:3b",
    totalTime: "108.77s",
  },
  {
    clinicalTone: "High",
    consistency: "Partial",
    exclusionLogic: "50%",
    jsonIntegrity: "100%",
    model: "llama3:8b",
    totalTime: "86.54s",
  },
  {
    clinicalTone: "High",
    consistency: "Partial",
    exclusionLogic: "50%",
    jsonIntegrity: "100%",
    model: "mistral-nemo:12b",
    totalTime: "95.83s",
  },
  {
    clinicalTone: "High",
    consistency: "High",
    exclusionLogic: "100%",
    jsonIntegrity: "100%",
    model: "qwen2.5:14b",
    totalTime: "216.72s",
    winner: true,
  },
  {
    clinicalTone: "High",
    consistency: "High",
    exclusionLogic: "100%",
    jsonIntegrity: "100%",
    model: "phi4:14b",
    totalTime: "194.86s",
  },
  {
    clinicalTone: "High",
    consistency: "High",
    exclusionLogic: "100%",
    jsonIntegrity: "100%",
    model: "llama-4-scout-17b",
    totalTime: "5.38s",
  },
  {
    clinicalTone: "High",
    consistency: "High",
    exclusionLogic: "100%",
    jsonIntegrity: "100%",
    model: "gpt-oss-120b",
    totalTime: "50.41s",
  },
];

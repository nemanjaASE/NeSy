export const navItems = [
  { href: "/#platform", label: "Platform" },
  { href: "/models", label: "Models" },
  { href: "/docs", label: "Docs" },
];

type HeroMetric = {
  countTo?: number;
  label: string;
  suffix?: string;
  tone: "blue" | "teal" | "violet";
  value: string;
};

export const heroMetrics: HeroMetric[] = [
  {
    label: "Medical Concepts",
    value: "15k+",
    countTo: 15000,
    suffix: "+",
    tone: "teal",
  },
  { label: "Deployment", value: "Local-first", tone: "blue" },
  { label: "Reasoning", value: "Explainable", tone: "violet" },
];

export const pipelineSteps = [
  "Narrative",
  "Symptoms",
  "Ontology",
  "Graph",
  "Explanation",
];

export const previewDiagnosis = {
  inputText:
    "I've been feeling very tired and nauseous for the past few days. My skin and eyes have turned yellow, and I noticed my stool has become pale and my urine is very dark. I do not feel drowsy and I am not confused.",
  presentSymptoms: ["fatigue", "nausea", "jaundice", "bloody stool", "dark urine"],
  absentSymptoms: ["drowsiness", "confusion"],
  mostLikely: "hepatitis E",
  confidence: "moderate",
  differentials: ["Epstein-Barr virus hepatitis", "hepatitis A"],
  excludedConditions: ["hepatitis D"],
  primaryAnalysis:
    "The patient's symptoms of fatigue, nausea, jaundice, and dark urine strongly align with the clinical presentation of hepatitis E. The majority of the reported symptoms are consistent with this disease, indicating a highly specific symptom profile.",
  differentialComparison: [
    {
      disease: "Epstein-Barr virus hepatitis",
      reasoning:
        "While Epstein-Barr virus hepatitis shares common symptoms such as fatigue and jaundice, it lacks additional distinctive features like dark urine that are more characteristic of hepatitis E. Additionally, fewer symptoms align with this condition compared to hepatitis E.",
    },
    {
      disease: "hepatitis A",
      reasoning:
        "Hepatitis A also presents with similar symptoms including fatigue, nausea, and jaundice but does not match the specific symptom of dark urine that is more indicative of hepatitis E. The alignment with other distinctive features of hepatitis E is stronger.",
    },
  ],
  exclusionCriteria: [
    {
      disease: "hepatitis D",
      reasoning:
        "Hepatitis D requires symptoms such as drowsiness and confusion, which the patient explicitly denied. These mandatory clinical markers negate the possibility of this condition being clinically consistent with the reported absences.",
    },
  ],
  recommendation: {
    specialistConsultations: ["gastroenterologist", "hepatologist"],
    labTests: [
      "liver function tests",
      "hepatitis E antibody test",
      "complete blood count",
    ],
    symptomsToVerify: [
      "abdominal pain",
      "joint pain",
      "fever",
      "loss of appetite",
      "vomiting",
      "liver inflammation",
    ],
  },
};

export const runtimePipeline = [
  {
    artifact: "present + absent symptoms",
    phase: "Extract",
    title: "Read the patient narrative",
    text: "The system turns free-form text into structured clinical findings, including symptoms the patient explicitly denies.",
  },
  {
    artifact: "mapped ontology symptoms",
    phase: "Map",
    title: "Map symptoms to ontology terms",
    text: "Extracted phrases are normalized against the symptom ontology so reasoning uses stable medical concepts.",
  },
  {
    artifact: "candidate diseases",
    phase: "Infer",
    title: "Search the disease graph",
    text: "Neo4j graph reasoning finds diseases connected to matched symptoms through ontology-backed has_symptom relations.",
  },
  {
    artifact: "ranked + filtered results",
    phase: "Score",
    title: "Score and filter candidates",
    text: "Candidates are ranked by symptom specificity, while explicitly absent symptoms block incompatible diseases.",
  },
  {
    artifact: "explanation + care plan",
    phase: "Explain",
    title: "Return transparent reasoning",
    text: "The UI receives the likely diagnosis, differentials, ruled-out conditions, and recommended next steps.",
  },
];

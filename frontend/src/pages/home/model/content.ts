export const navItems = ["Platform", "Workflow", "Models", "Docs"];

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
  differentials: [
    "Epstein-Barr virus hepatitis",
    "hepatitis A",
    "hepatitis B",
    "hepatitis C",
  ],
  excludedConditions: ["hepatitis D"],
  primaryAnalysis:
    "The patient's symptoms of fatigue, nausea, jaundice, and dark urine strongly align with the clinical presentation of hepatitis E. The majority of the reported symptoms are consistent with this condition, indicating a high specificity for hepatitis E.",
  differentialComparison: [
    {
      disease: "Epstein-Barr virus hepatitis",
      reasoning:
        "While Epstein-Barr virus hepatitis shares some common symptoms such as fatigue and jaundice, it lacks additional distinctive features like dark urine that are more characteristic of hepatitis E. The alignment with the patient's profile is less comprehensive compared to hepatitis E.",
    },
    {
      disease: "hepatitis A",
      reasoning:
        "Hepatitis A also presents with similar symptoms including fatigue, nausea, and jaundice but lacks additional specific markers found in the patient's profile that are more indicative of hepatitis E. The overall symptom alignment is less robust compared to hepatitis E.",
    },
    {
      disease: "hepatitis B",
      reasoning:
        "Hepatitis B shares common symptoms like fatigue, nausea, and jaundice with the patient's presentation but does not have additional distinctive features seen in hepatitis E. Therefore, it has a lower clinical alignment than hepatitis E.",
    },
    {
      disease: "hepatitis C",
      reasoning:
        "Similar to other differentials, hepatitis C presents with common symptoms such as fatigue, nausea, and jaundice but lacks the specific markers like dark urine that are more characteristic of hepatitis E. The overall symptom profile is less aligned compared to hepatitis E.",
    },
  ],
  exclusionCriteria: [
    {
      disease: "hepatitis D",
      reasoning:
        "Hepatitis D requires symptoms such as drowsiness and confusion, which the patient explicitly denied. These mandatory clinical markers negate the possibility of this condition in the current context.",
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

export const workflowCards = [
  {
    title: "Extract symptoms",
    text: "Convert patient narratives into structured, present and absent clinical findings.",
  },
  {
    title: "Ground concepts",
    text: "Map extracted phrases to standard medical ontologies before running graph inference.",
  },
  {
    title: "Explain results",
    text: "Deliver ranked diagnostic candidates with transparent reasoning, exclusions, and next steps.",
  },
];

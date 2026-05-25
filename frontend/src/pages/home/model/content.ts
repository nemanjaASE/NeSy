export const navItems = ["Platform", "Workflow", "Models", "Docs"];

export const heroMetrics = [
  {
    label: "Medical Concepts",
    value: "15k+",
    countTo: 15000,
    suffix: "+",
  },
  { label: "Deployment", value: "Local-first" },
  { label: "Reasoning", value: "Explainable" },
];

export const findings = [
  { label: "Present", value: "rash, itching, redness", tone: "green" },
  { label: "Absent", value: "fever, fatigue, joint pain", tone: "red" },
  { label: "Candidate", value: "contact dermatitis", tone: "lime" },
];

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

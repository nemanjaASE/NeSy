export type DiagnosticRequest = {
  text: string;
};

export type DifferentialComparison = {
  disease: string;
  reasoning: string;
};

export type ExclusionCriteria = {
  excluded_disease: string;
  reasoning: string;
};

export type XaiReasoning = {
  primary_analysis: string;
  differential_comparison: DifferentialComparison[];
  exclusion_criteria: ExclusionCriteria[];
};

export type Recommendation = {
  specialist_consultations: string[];
  lab_tests: string[];
  symptoms_to_verify: string[];
};

export type XaiExplanation = {
  most_likely: string;
  confidence: string;
  differentials: string[];
  excluded_conditions: string[];
  reasoning: XaiReasoning;
  recommendation: Recommendation;
};

export type DiagnosticResponse = {
  input_text: string;
  present_symptoms: string[];
  absent_symptoms: string[];
  explanation: XaiExplanation;
};

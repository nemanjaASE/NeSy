from pydantic import BaseModel, Field
from typing import List, Literal

EmbeddingVector = List[float]
EmbeddingMatrix = List[EmbeddingVector]

class SymptomOntologyData(BaseModel):
    """
    Represents a single symptom entry from the medical ontology knowledge graph.

    Attributes:
        label:     The human-readable name of the symptom as defined in the ontology.
        embedding: The pre-computed vector representation of the symptom label,
                   used for semantic similarity matching.
    """

    label:     str
    embedding: EmbeddingVector

class SemanticMatchResult(BaseModel):
    """
    Represents the result of mapping a single patient-reported symptom
    to its closest ontological term via vector similarity search.

    Attributes:
        input_symptom:  The raw symptom term extracted from the patient's input.
        mapped_symptom: The closest matching term found in the ontology.
        confidence:     Cosine similarity score between the input and ontology embeddings (0.0 - 1.0).
        kind:           Indicates whether the symptom is reported as present or absent by the patient.
        is_match:       True if the confidence score meets or exceeds the similarity threshold.
    """

    input_symptom:  str
    mapped_symptom: str
    confidence:     float = Field(..., ge=0.0, le=1.0)
    kind:           Literal["present", "absent"]
    is_match:       bool

class ExtractedSymptoms(BaseModel):
    """
    Structured output of the NLP symptom extraction step.

    Attributes:
        present: Symptoms the patient explicitly reports having.
        absent:  Symptoms the patient explicitly denies having.
    """
    present: List[str]
    absent:  List[str]


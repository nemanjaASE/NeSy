from typing import Protocol
from ..models.result import Result
from ..models.symptom import ExtractedSymptoms


class NLPExtractor(Protocol):
    """
    Interface defining the contract for NLP-based symptom extraction from raw clinical text.

    Any infrastructure implementation (Groq, Ollama, OpenAI, etc.) must fulfill
    this interface to be used within the diagnostic pipeline.
    """

    async def extract_symptoms(self, text: str) -> Result[ExtractedSymptoms]:
        """
        Extract clinically relevant symptoms from a patient's free-text description.

        The implementation is expected to distinguish between symptoms the patient
        reports as present and those they explicitly deny, returning both as structured output.

        Args:
            text: Raw clinical description provided by the patient in natural language.

        Returns:
            Result[ExtractedSymptoms]: A structured object containing:
                - present: symptoms the patient confirms having
                - absent:  symptoms the patient explicitly denies
        """
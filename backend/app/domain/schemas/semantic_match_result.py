from pydantic import BaseModel

class SemanticMatchResult(BaseModel):
    """
    Details about each symptom match, including the original input, the mapped ontology term, confidence score, and whether it was considered a match based on the threshold.
    """
    input_symptom: str
    mapped_symptom: str
    confidence: float
    is_match: bool
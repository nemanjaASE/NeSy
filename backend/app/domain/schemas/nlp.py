from pydantic import BaseModel, Field
from typing import List

class EntityExtraction(BaseModel):
    """
    Result of the NLP extraction phase.
    """
    entities: List[str] = Field(..., description="List of medical terms found.")
    raw_text: str = Field(..., description="The original input.")
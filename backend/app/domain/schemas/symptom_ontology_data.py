from pydantic import BaseModel
from typing import List

class SymptomOntologyData(BaseModel):
    label: str
    embedding: List[float]
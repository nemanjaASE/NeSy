from typing import Protocol, List, Dict, Any
from ..models.result import Result
from ..models.explanation import XAIExplanationResult

class DiagnosticExplainer(Protocol):
    """
    Domain interface for generating Explainable AI (XAI) reasoning 
    based on neuro-symbolic inference results.
    """
    
    async def generate_explanation(self, disease_results: List[Dict[str, Any]], max_retries: int = 3) -> Result[XAIExplanationResult]:
        """
        Generates human-readable reasoning for the predicted diseases.
        """
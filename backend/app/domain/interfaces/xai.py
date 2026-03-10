from typing import Protocol, List, Dict, Any

class DiagnosticExplainer(Protocol):
    """
    Domain interface for generating Explainable AI (XAI) reasoning 
    based on neuro-symbolic inference results.
    """
    
    async def generate_explanation(self, disease_results: List[Dict[str, Any]], max_retries: int = 3) -> Dict[str, Any]:
        """
        Generates human-readable reasoning for the predicted diseases.
        """
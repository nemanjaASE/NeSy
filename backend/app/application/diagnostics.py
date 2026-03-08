from typing import List
from app.domain.interfaces import NLPExtractor
from app.core import logger

class DiagnosticCoordinator:
    """
    Coordinator responsible for the diagnostic workflow.
    """

    def __init__(self, nlp_extractor: NLPExtractor):
        """
        Initialize the coordinator with domain interfaces.
        """
        self.nlp_extractor = nlp_extractor

    async def run_extraction_pipeline(self, text: str) -> List[str]:
        """
        Run the first stage of the pipeline: Symptom Extraction.
        
        Args:
            text (str): Patient's input.
            
        Returns:
            List[str]: List of identified clinical symptoms.
        """
        logger.info("Executing extraction pipeline.")
        return await self.nlp_extractor.extract_entities(text)
from typing import Protocol, List, Tuple

class NLPExtractor(Protocol):
    """
    Interface for extracting clinical entities from raw medical text.
    """

    async def extract_entities(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Extract present and absent symptoms from the input string using an LLM.

        Args:
            text (str): The raw clinical description provided by the user.

        Returns:
            Tuple[List[str], List[str]]: A tuple of (present_symptoms, absent_symptoms).
        """
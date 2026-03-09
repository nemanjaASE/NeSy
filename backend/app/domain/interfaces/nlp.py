from typing import Protocol, List

class NLPExtractor(Protocol):
    """
    Interface for extracting clinical entities from raw medical text.
    """

    async def extract_entities(self, text: str) -> List[str]:
        """
        Extract symptoms or disease names from the input string using an LLM.

        Args:
            text (str): The raw clinical description provided by the user.

        Returns:
            List[str]: A list of extracted symptom names.
        """
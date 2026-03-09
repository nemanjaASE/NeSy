import json
from typing import List
from groq import Groq
from app.domain.interfaces.nlp import NLPExtractor
from app.core.config import settings
from app.core.logger import logger
from .prompt_loader import load_prompt

class GroqNLPExtractor(NLPExtractor):
    """
    Infrastructure implementation of NLPExtractor using Groq Cloud API.
    This class handles the communication with the LLM to extract symptoms.
    """

    def __init__(self):
        """
        Initialize the Groq client and load configuration.
        """
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_EXTRACTION_MODEL_NAME
        self.system_prompt = load_prompt("symptom_extraction_prompt.txt")

    async def extract_entities(self, text: str) -> List[str]:
        """
        Send the user input to Groq LLM and parse the extracted symptoms.

        Args:
            text (str): Raw clinical text from the patient.

        Returns:
            List[str]: A list of extracted symptom names.
        """
        try:
            logger.info(f"Extracting symptoms using model: {self.model}")
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                model=self.model,
                temperature=0.0,
                response_format={"type": "json_object"}
            )

            content = chat_completion.choices[0].message.content
            data = json.loads(content)
            
            symptoms = data.get("symptoms", [])
            
            logger.info(f"Extraction successful. Found {len(symptoms)} symptoms.")
            return symptoms

        except Exception as e:
            logger.error(f"Error during Groq symptom extraction: {str(e)}")
            return []
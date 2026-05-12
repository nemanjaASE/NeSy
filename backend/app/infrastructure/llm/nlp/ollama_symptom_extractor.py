import json
import re
import logging
from openai import AsyncOpenAI
from app.domain import NLPExtractor, ExtractedSymptoms
from app.core import settings, timed
from ..prompt_loader import load_prompt
from ..constants import SYMPTOM_EXTRACTION_PROMPT, NLP_SUBFOLDER

logger = logging.getLogger(__name__)

class OllamaSymptomExtractor(NLPExtractor):
    """
    NLPExtractor implementation backed by a locally hosted Ollama instance.

    Communicates with Ollama via its OpenAI-compatible REST API, enabling
    fully offline inference without reliance on external cloud services.
    Intended for local development or privacy-sensitive deployments.
    """

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY
        )
        self.model = settings.LLM_EXTRACTION_MODEL_NAME
        self.system_prompt = load_prompt(SYMPTOM_EXTRACTION_PROMPT, NLP_SUBFOLDER)

    @timed("Ollama Symptom Extraction")
    async def extract_symptoms(self, text: str) -> ExtractedSymptoms:
        """
        Send patient input to the local Ollama model and parse the symptom extraction response.

        Since local models may wrap JSON in additional text, a regex fallback is applied
        to extract the JSON object if direct parsing fails. Returns an empty
        ExtractedSymptoms object on any failure to allow the pipeline to continue gracefully.

        Args:
            text: Raw clinical description provided by the patient.

        Returns:
            ExtractedSymptoms: Extracted present and absent symptoms.
        """
        try:
            logger.info(f"Extracting symptoms using Ollama model: {self.model}")

            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user",   "content": text}
                ],
                temperature=settings.LLM_EXTRACTION_TEMPERATURE,
                top_p=settings.LLM_EXTRACTION_TOP_P,
                max_tokens=settings.LLM_EXTRACTION_MAX_TOKENS,
                seed=settings.LLM_EXTRACTION_SEED,
                stream=settings.LLM_STREAM,
            )

            raw = completion.choices[0].message.content

            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not match:
                logger.warning("No JSON found in Ollama response.")
                return ExtractedSymptoms(present=[], absent=[])

            result = json.loads(match.group())

            return ExtractedSymptoms(present=result.get("present", []), absent=result.get("absent", []))

        except Exception as e:
            logger.error(f"Error during Ollama symptom extraction: {str(e)}")
            return ExtractedSymptoms(present=[], absent=[])
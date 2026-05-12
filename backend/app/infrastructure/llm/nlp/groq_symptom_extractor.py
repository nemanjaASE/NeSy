import json
import logging
from groq import AsyncGroq
from app.domain import NLPExtractor, ExtractedSymptoms
from app.core import settings, timed
from ..prompt_loader import load_prompt
from ..constants import SYMPTOM_EXTRACTION_PROMPT, NLP_SUBFOLDER

logger = logging.getLogger(__name__)

class GroqSymptomExtractor(NLPExtractor):
    """
    NLPExtractor implementation backed by the Groq Cloud API.

    Uses a instruction-tuned LLM to parse a patient's free-text input and
    extract structured symptom data. Intended for cloud-based deployments
    where low-latency inference is required.
    """

    def __init__(self):
        self.client = AsyncGroq(api_key=settings.LLM_API_KEY)
        self.model = settings.LLM_EXTRACTION_MODEL_NAME
        self.system_prompt = load_prompt(SYMPTOM_EXTRACTION_PROMPT, NLP_SUBFOLDER)

    @timed("Groq Symptom Extraction")
    async def extract_symptoms(self, text: str) -> ExtractedSymptoms:
        """
        Send patient input to the Groq LLM and parse the symptom extraction response.

        The model is prompted to return a JSON object. If parsing fails or the
        API call raises an exception, an empty ExtractedSymptoms object is returned
        to allow the pipeline to continue gracefully.

        Args:
            text: Raw clinical description provided by the patient.

        Returns:
            ExtractedSymptoms: Extracted present and absent symptoms.
        """
        try:
            logger.info(f"Extracting symptoms using Groq model: {self.model}")

            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user",   "content": text}
                ],
                model=self.model,
                temperature=settings.LLM_EXTRACTION_TEMPERATURE,
                top_p=settings.LLM_EXTRACTION_TOP_P,
                max_tokens=settings.LLM_EXTRACTION_MAX_TOKENS,
                seed=settings.LLM_EXTRACTION_SEED,
                response_format=({"type": "json_object"} if settings.LLM_EXTRACTION_FORCE_JSON else {})

            )

            content = chat_completion.choices[0].message.content
            data = json.loads(content)

            return ExtractedSymptoms(present=data.get("present", []), absent=data.get("absent", []))

        except Exception as e:
            logger.error(f"Error during Groq symptom extraction: {str(e)}")
            return ExtractedSymptoms(present=[], absent=[])
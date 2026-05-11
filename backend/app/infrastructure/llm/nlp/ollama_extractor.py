from openai import AsyncOpenAI
import json, re
from typing import List, Tuple
from app.domain import NLPExtractor
from app.core import settings, logger
from ..prompt_loader import load_prompt

class OllamaNLPExtractor(NLPExtractor):

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key="ollama"
        )
        self.model = settings.LLM_EXTRACTION_MODEL_NAME
        self.system_prompt = load_prompt("symptom_extraction_prompt.txt")

    async def extract_entities(self, text: str) -> Tuple[List[str], List[str]]:
        try:
            logger.info(f"Extracting symptoms using Ollama model: {self.model}")

            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user",   "content": text}
                ],
                temperature=0.0,
                top_p=1,
                max_tokens=1500,
                seed=42,
                stream=False,
            )

            raw = completion.choices[0].message.content

            match = re.search(r'\{.*\}', raw, re.DOTALL)
            
            if not match:
                logger.warning("No JSON found in Ollama response.")
                return [], []

            result = json.loads(match.group())

            present = result.get("present", [])
            absent  = result.get("absent", [])

            logger.info(f"Found {len(present)} present, {len(absent)} absent symptoms.")
            return present, absent

        except Exception as e:
            logger.error(f"Error during Ollama symptom extraction: {str(e)}")
            return [], []
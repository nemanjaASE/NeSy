import re
import json
import asyncio
import logging
from openai import AsyncOpenAI
from app.core import settings, timed
from app.domain import XAIExplanationResult, DiagnosisResult, DiseaseInference
from ..constants import DISEASE_EXPLANATION_PROMPT, XAI_SUBFOLDER
from ..prompt_loader import load_prompt

logger = logging.getLogger(__name__)

class OllamaExplainer:
    """
    Explainable AI (XAI) layer that uses an LLM to generate human-readable
    reasoning for the neuro-symbolic diagnostic results.
    """

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key="ollama"
        )
        self.model = settings.LLM_XAI_MODEL_NAME
        self.system_prompt = load_prompt(DISEASE_EXPLANATION_PROMPT, XAI_SUBFOLDER)

    def _format_input(self, diagnosis_result: DiagnosisResult) -> str:
        """Formats DiagnosisResult into a prompt-friendly string."""
        lines = []

        for r in diagnosis_result.included:
            lines.append(self._format_disease(r, passed_filter=True))

        for r in diagnosis_result.excluded:
            lines.append(self._format_disease(r, passed_filter=False))

        return "\n".join(lines)

    def _format_disease(self, r: DiseaseInference, passed_filter: bool) -> str:
        return (
            f"- {r.disease_name} (\n"
            f"  URI: {r.uri},\n"
            f"  Normalized Score: {round(r.normalized_score, 4)},\n"
            f"  Filter Status: {passed_filter},\n"
            f"  Match Count: {r.match_count},\n"
            f"  Disease Coverage: {r.disease_coverage_pct}%,\n"
            f"  Input Coverage: {r.input_coverage_pct}%,\n"
            f"  Blocking Symptoms: {r.blocking_symptoms},\n"
            f"  Matched List: {r.matched_symptoms},\n"
            f"  Missing List: {r.missing_symptoms})\n"
        )

    @timed("LLM Explanation Generation")
    async def generate_explanation(
        self,
        diagnosis_result: DiagnosisResult,
        max_retries: int = 3
    ) -> XAIExplanationResult:
        """
        Calls the LLM to generate reasoning based on scored and filtered diseases.
        """
        if not diagnosis_result.included and not diagnosis_result.excluded:
            logger.warning("No disease results provided to XAI layer.")
            return XAIExplanationResult.fallback("No data for reasoning.")

        formatted_input = self._format_input(diagnosis_result)
        logger.debug(f"Sending {len(diagnosis_result.included)} included and {len(diagnosis_result.excluded)} excluded diseases to XAI.")

        for attempt in range(max_retries):
            try:
                completion = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user",   "content": formatted_input}
                    ],
                    temperature=settings.LLM_XAI_TEMPERATURE,
                    top_p=settings.LLM_XAI_TOP_P,
                    max_tokens=settings.LLM_XAI_MAX_TOKENS,
                    seed=settings.LLM_XAI_SEED,
                    stream=settings.LLM_XAI_STREAM,
                    response_format=({"type": "json_object"} if settings.LLM_XAI_FORCE_JSON else {} ),
                )

                raw = completion.choices[0].message.content

                try:
                    result = json.loads(raw)
                    logger.info(f"XAI response parsed successfully on attempt {attempt + 1}.")
                    return XAIExplanationResult.model_validate(result)
                except json.JSONDecodeError:
                    pass

                match = re.search(r'\{.*\}', raw, re.DOTALL)
                if match:
                    result = json.loads(match.group())
                    logger.info(f"XAI response parsed via regex fallback on attempt {attempt + 1}.")
                    return XAIExplanationResult.model_validate(result)

                logger.warning(f"Attempt {attempt + 1}/{max_retries} did not return valid JSON. Retrying...")
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Error during XAI API call on attempt {attempt + 1}/{max_retries}: {str(e)}")
                await asyncio.sleep(1)

        logger.error("All XAI attempts failed.")
        return XAIExplanationResult.fallback("Technical error during reasoning generation.")
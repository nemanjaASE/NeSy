import json
import re
import asyncio
from typing import List, Dict, Any
from groq import AsyncGroq
from app.core import logger, settings
from .prompt_loader import load_prompt

class XAIExplainer:
    """
    Explainable AI (XAI) layer that uses an LLM to generate human-readable 
    reasoning for the neuro-symbolic diagnostic results.
    """

    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_XAI_MODEL_NAME
        self.system_prompt = load_prompt("disease_explanation_prompt.txt")

    def _format_input(self, disease_results: List[Dict[str, Any]]) -> str:
        """Formats the inference results into a prompt-friendly string."""
        lines = []
        for r in disease_results:
            missing = r.get("missing_symptoms", [])
            missing_str = ", ".join(missing) if missing else "none"
            lines.append(
                f"- {r.get('disease_name', 'Unknown')} ("
                f"uri: {r.get('uri', 'N/A')}, "
                f"score: {r.get('normalized_score', 0)}, "
                f"matched: {r.get('match_count', 0)} symptoms, "
                f"disease_coverage: {r.get('disease_coverage_pct', 'N/A')}, "
                f"input_coverage: {r.get('input_coverage_pct', 'N/A')}, "
                f"matched_symptoms: {r.get('matched_symptoms', [])}, "
                f"missing_symptoms: [{missing_str}])"
            )
        return "\n".join(lines)

    async def generate_explanation(self, disease_results: List[Dict[str, Any]], max_retries: int = 3) -> Dict[str, Any]:
        """
        Calls the LLM to generate reasoning based on the extracted and scored diseases.
        """
        if not disease_results:
            logger.warning("No disease results provided to XAI layer.")
            return self._get_fallback_response("No data available for reasoning.")

        formatted_input = self._format_input(disease_results)
        logger.debug(f"Sending formatted data to LLM: {len(disease_results)} diseases.")

        for attempt in range(max_retries):
            try:
                completion = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": formatted_input}
                    ],
                    temperature=0.1,
                    top_p=1.0,
                    max_tokens=2500,
                    stream=False,
                    response_format={"type": "json_object"},
                )

                raw = completion.choices[0].message.content
                
                try:
                    result = json.loads(raw)
                    logger.info(f"Successfully generated XAI response on attempt {attempt + 1}.")
                    return result
                except json.JSONDecodeError:
                    pass

                match = re.search(r'\{.*\}', raw, re.DOTALL)
                if match:
                    result = json.loads(match.group())
                    logger.info(f"Successfully recovered XAI JSON using regex on attempt {attempt + 1}.")
                    return result

                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed to return valid JSON. Retrying...")
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Error during LLM API call on attempt {attempt + 1}/{max_retries}: {str(e)}")
                await asyncio.sleep(1)
                
        logger.error("All attempts to generate XAI reasoning have failed.")
        return self._get_fallback_response("Failed to generate reasoning due to technical limitations.")

    def _get_fallback_response(self, reason: str) -> Dict[str, Any]:
        """Returns a safe default response if the LLM completely fails."""
        return {
            "most_likely": "unknown",
            "confidence": "low",
            "differentials": [],
            "reasoning": reason,
            "recommendation": "Please consult a healthcare professional for clinical evaluation."
        }
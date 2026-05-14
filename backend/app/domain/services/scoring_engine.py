import logging
from ..models.disease import RawDiseaseMatch, DiagnosisResult
from ..models.result import Result
from ..services.disease_filter import DiseaseFilter
from ..services.disease_ranker import DiseaseRanker
from ..services.disease_scorer import DiseaseScorer

logger = logging.getLogger(__name__)


class ScoringEngine:
    """
    Domain service that orchestrates the disease candidate evaluation pipeline.

    Acts as a facade over three focused domain services:
        - DiseaseScorer:  calculates coverage and normalized scores per candidate
        - DiseaseFilter:  separates candidates into included and excluded groups
        - DiseaseRanker:  sorts and trims each group by score and configured limits

    This class contains no scoring logic itself — it only defines the order
    of operations and wires the services together.
    """

    def __init__(
        self,
        scorer: DiseaseScorer,
        filter: DiseaseFilter,
        ranker: DiseaseRanker,
    ):
        self.scorer = scorer
        self.filter = filter
        self.ranker = ranker

    def evaluate(
        self, raw_records: list[RawDiseaseMatch], total_input_symptoms: int
    ) -> Result[DiagnosisResult]:
        """
        Run the full disease candidate evaluation pipeline.

        Args:
            raw_records:          Raw disease candidates returned by Neo4j inference query.
            total_input_symptoms: Total number of present symptoms provided by the patient,
                                  used to calculate input coverage percentage.

        Returns:
            Result[DiagnosisResult]: Success with ranked included and excluded disease
            candidates, or failure with an error message.
        """
        if not raw_records:
            logger.warning("No raw records provided to scoring engine.")
            return Result.failure("No disease candidates to evaluate.")

        try:
            scored = self.scorer.score_all(raw_records, total_input_symptoms)
            included, excluded = self.filter.split(scored, raw_records)
            result = self.ranker.rank(included, excluded)

            logger.info(
                f"Scoring complete. Included: {len(result.included)}, Excluded: {len(result.excluded)}."
            )
            return Result.success(result)

        except Exception as e:
            logger.exception("Scoring engine evaluation failed.")
            return Result.failure(f"Scoring engine failed: {str(e)}")

from typing import List, Tuple
from app.domain import RawDiseaseMatch, DiseaseInference

class DiseaseFilter:
    def split(
        self,
        scored: List[DiseaseInference],
        raw_records: List[RawDiseaseMatch]
    ) -> Tuple[List[DiseaseInference], List[DiseaseInference]]:
        passed = {rec.disease for rec in raw_records if rec.passed_filter}

        included = [d for d in scored if d.disease_name in passed]
        excluded = [d for d in scored if d.disease_name not in passed]

        return included, excluded
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from ..schemas import SemanticMatchResult

class SemanticMatcher:
    """
    Domain Service responsible for mapping symptoms using vector similarity.
    """

    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold

    def find_best_matches(
        self, 
        query_embeddings: List[List[float]], 
        onto_labels: List[str], 
        onto_vectors: List[List[float]],
        original_terms: List[str]
    ) -> List[SemanticMatchResult]:
        """
        Calculates cosine similarity between query embeddings and ontology vectors to find the best matches.
        Args:
            query_embeddings: List of vector embeddings for the input symptoms.
            onto_labels: List of symptom labels from the ontology.
            onto_vectors: List of vector embeddings for the ontology symptoms.
            original_terms: List of original symptom terms corresponding to the query embeddings.
        Returns:
            A list of SemanticMatchResult objects containing the input symptom, mapped symptom, confidence score, and match status.
        """
        if not query_embeddings or not onto_vectors:
            return []

        q_vecs = np.array(query_embeddings)
        o_vecs = np.array(onto_vectors)

        matrix = cosine_similarity(q_vecs, o_vecs)

        results = []
        for i, term in enumerate(original_terms):
            scores = matrix[i]
            best_idx = np.argmax(scores)
            confidence = float(scores[best_idx])

            results.append(SemanticMatchResult(
                input_symptom=term,
                mapped_symptom=onto_labels[best_idx],
                confidence=confidence,
                is_match=confidence >= self.threshold
            ))
            
        return results
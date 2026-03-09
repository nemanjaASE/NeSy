from fastapi import APIRouter, Depends, Request
from app.domain.schemas import DiagnosticRequest
from app.application import DiagnosticCoordinator
from app.domain import NLPExtractor, TextEmbedder, SemanticMatcher, DiagnosticResult, DiseaseScorer

router = APIRouter()

def get_nlp_extractor(request: Request) -> NLPExtractor:
    return request.app.state.nlp_extractor

def get_embedder(request: Request) -> TextEmbedder:
    return request.app.state.embedder

def get_coordinator(request: Request) -> DiagnosticCoordinator:
    return DiagnosticCoordinator(
        nlp_extractor=request.app.state.nlp_extractor,
        embedder=request.app.state.embedder,
        matcher=SemanticMatcher(threshold=0.9),
        scorer=DiseaseScorer(top_k=5),
        repository=request.app.state.db
    )

@router.post("/diagnose", response_model=DiagnosticResult)
async def perform_diagnosis(
    request: Request,
    payload: DiagnosticRequest,
    coordinator: DiagnosticCoordinator = Depends(get_coordinator),
):
    """
    Endpoint to extract symptoms from raw medical text.
    """
    onto_labels = request.app.state.onto_labels
    onto_vectors = request.app.state.onto_vectors

    results = await coordinator.run_full_diagnostic_pipeline(
        text=payload.text,
        onto_labels=onto_labels,
        onto_vectors=onto_vectors
    )
    
    return {
        "input_text": payload.text,
        "extracted_entities": [m["input_symptom"] for m in results["raw_matches"]],
        "ontological_matches": results["mapped_symptoms"],
        "detailed_results": results["raw_matches"],
        "inference": {
            "total_input_symptoms": len(results["mapped_symptoms"]),
            "diseases": results["inference"]["diseases"]
        }
    }
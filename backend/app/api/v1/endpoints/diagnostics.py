from fastapi import APIRouter, Depends, Request
from app.domain.schemas import DiagnosticRequest
from app.application import DiagnosticCoordinator
from app.domain import NLPExtractor, TextEmbedder, SemanticMatcher, DiagnosticResult

router = APIRouter()

def get_nlp_extractor(request: Request) -> NLPExtractor:
    return request.app.state.nlp_extractor

def get_embedder(request: Request) -> TextEmbedder:
    return request.app.state.embedder

@router.post("/extract", response_model=DiagnosticResult)
async def extract_symptoms(
    request: Request,
    payload: DiagnosticRequest,
    extractor: NLPExtractor = Depends(get_nlp_extractor),
    embedder: TextEmbedder = Depends(get_embedder)
):
    """
    Endpoint to extract symptoms from raw medical text.
    """
    onto_labels = request.app.state.onto_labels
    onto_vectors = request.app.state.onto_vectors

    matcher = SemanticMatcher(threshold=0.85)

    coordinator = DiagnosticCoordinator(
        nlp_extractor=extractor,
        embedder=embedder,
        matcher=matcher
    )
    
    results = await coordinator.run_full_diagnostic_pipeline(
        text=payload.text,
        onto_labels=onto_labels,
        onto_vectors=onto_vectors
    )
    
    return {
        "input_text": payload.text,
        "extracted_entities": [m["input_symptom"] for m in results["raw_matches"]],
        "ontological_matches": results["final_symptoms"],
        "detailed_results": results["raw_matches"]
    }
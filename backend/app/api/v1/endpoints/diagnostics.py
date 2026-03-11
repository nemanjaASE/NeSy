from fastapi import APIRouter, Depends, Request
from app.domain import NLPExtractor, TextEmbedder, SemanticMatcher, DiagnosticResponseDTO, DiseaseScorer, DiagnosticRequestDTO
from app.application import DiagnosticCoordinator

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
        repository=request.app.state.db,
        xai_explainer=request.app.state.xai_explainer
    )

@router.post("/diagnose", response_model=DiagnosticResponseDTO)
async def perform_diagnosis(
    request: Request,
    payload: DiagnosticRequestDTO,
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
    
    return results
from fastapi import APIRouter, Depends, Request
from app.domain import DiagnosticResponseDTO, DiagnosticRequestDTO
from app.application import DiagnosticCoordinator

router = APIRouter()


def get_coordinator(request: Request) -> DiagnosticCoordinator:
    return DiagnosticCoordinator(
        nlp_extractor=request.app.state.nlp_extractor,
        embedder=request.app.state.embedder,
        matcher=request.app.state.semantic_matcher,
        scoring_engine=request.app.state.scoring_engine,
        repository=request.app.state.db,
        xai_explainer=request.app.state.xai_explainer,
    )


@router.post("/diagnose", response_model=DiagnosticResponseDTO)
async def perform_diagnosis(
    request: Request,
    payload: DiagnosticRequestDTO,
    coordinator: DiagnosticCoordinator = Depends(get_coordinator),
):
    """
    Perform a full diagnostic pipeline run for the given patient input.

    Extracts symptoms from raw text, maps them to ontological terms,
    infers disease candidates from the knowledge graph, scores and ranks
    them, and returns an AI-generated clinical explanation.
    """
    return await coordinator.run_full_diagnostic_pipeline(
        text=payload.text,
        onto_labels=request.app.state.onto_labels,
        onto_vectors=request.app.state.onto_vectors,
    )

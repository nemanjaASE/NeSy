from fastapi import APIRouter, Depends, Request
from app.domain.schemas import DiagnosticRequest, EntityExtraction
from app.application import DiagnosticCoordinator
from app.domain.interfaces import NLPExtractor

router = APIRouter()

def get_nlp_extractor(request: Request) -> NLPExtractor:
    return request.app.state.nlp_extractor

@router.post("/extract", response_model=EntityExtraction)
async def extract_symptoms(
    payload: DiagnosticRequest,
    extractor: NLPExtractor = Depends(get_nlp_extractor)
):
    """
    Endpoint to extract symptoms from raw medical text.
    """
    coordinator = DiagnosticCoordinator(extractor)
    
    symptoms = await coordinator.run_extraction_pipeline(payload.text)
    
    return EntityExtraction(
        entities=symptoms,
        raw_text=payload.text
    )
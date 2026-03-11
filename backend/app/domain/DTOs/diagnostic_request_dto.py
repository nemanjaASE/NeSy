from pydantic import BaseModel, Field

class DiagnosticRequestDTO(BaseModel):
    """
    The initial input from the user/patient.
    """
    text: str = Field(..., example="Već par dana kašljem i imam baš visoku temperaturu.")

from pydantic import BaseModel, Field

class DiagnosticRequest(BaseModel):
    """
    The initial input from the user/patient.
    """
    text: str = Field(..., example="I have a sharp pain in my lower back.")
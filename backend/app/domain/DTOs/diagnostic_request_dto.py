from pydantic import BaseModel, Field


class DiagnosticRequestDTO(BaseModel):
    """
    The initial input from the user/patient.
    """

    text: str = Field(
        ...,
        example="I have a rash on my chest and arms, it itches and is red — but no fever, no fatigue, no joint pain.",
    )

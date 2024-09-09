from pydantic import BaseModel, Field
from typing import List

from .orbits import GeneralPerturbationsOrbitState
from .utils import Identifier


class Payload(BaseModel):
    id: Identifier = Field(..., description="Payload identifier.")
    field_of_view: float = Field(
        gt=0, le=180, description="Angular payload field of view."
    )


class Satellite(BaseModel):
    id: Identifier = Field(..., description="Satellite identifier.")
    orbit: GeneralPerturbationsOrbitState = Field(
        ..., description="Initial orbit state."
    )
    payloads: List[Payload] = Field([], description="Satellite payloads.")

from pydantic import BaseModel, Field
from typing import List

from .orbits import GeneralPerturbationsOrbitState
from .utils import Identifier


class Instrument(BaseModel):
    id: Identifier = Field(..., description="Instrument identifier.")
    field_of_view: float = Field(
        gt=0, le=180, description="Angular instrument field of view."
    )


class Satellite(BaseModel):
    id: Identifier = Field(..., description="Satellite identifier.")
    orbit: GeneralPerturbationsOrbitState = Field(
        ..., description="Initial orbit state."
    )
    instruments: List[Instrument] = Field([], description="Satellite instruments.")

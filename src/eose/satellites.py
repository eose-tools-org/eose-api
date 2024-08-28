from pydantic import BaseModel, Field

from .orbits import GeneralPerturbationsOrbitState
from .utils import Identifier


class Satellite(BaseModel):
    id: Identifier = Field(..., description="Satellite identifier.")
    orbit: GeneralPerturbationsOrbitState = Field(
        ..., description="Initial orbit state."
    )
    field_of_view: float = Field(
        gt=0, le=180, description="Angular instrument field of view."
    )

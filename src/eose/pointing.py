from typing import List, Optional, Union

from pydantic import Field

from .utils import Quaternion, FixedOrientation
from .propagation import PropagationRecord, PropagationResponse

class PointingRequest(PropagationResponse):
    mode: Union[FixedOrientation] = Field(
        FixedOrientation.NADIR_GEOCENTRIC, description="Pointing mode."
    )


class PointingRecord(PropagationRecord):
    body_orientation: Optional[Union[FixedOrientation, Quaternion]] = Field(
        None,
        description="Orientation of the spacecraft body-fixed frame, relative to requested frame.",
    )
    view_orientation: Optional[Quaternion] = Field(
        [0, 0, 0, 1],
        description="Orientation of the instrument view, relative to the body-fixed frame.",
    )


class PointingResponse(PointingRequest):
    time_series: List[PointingRecord] = Field([], description="Pointing results")
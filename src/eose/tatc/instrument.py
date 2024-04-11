# -*- coding: utf-8 -*-
"""
Object schemas for instruments.

@author: Paul T. Grogan <paul.grogan@asu.edu>
"""

from typing import Optional
from datetime import timedelta

from pydantic import BaseModel, Field


class Instrument(BaseModel):
    """
    Remote sensing instrument.
    """

    name: str = Field(..., description="Instrument name.")
    field_of_regard: float = Field(
        180,
        description="Angular field (degrees) of possible observations (with pointing).",
        gt=0,
        le=360,
        examples=[50],
    )
    min_access_time: timedelta = Field(
        timedelta(0),
        description="Minimum access (integration) time to record an observation.",
        examples=[timedelta(seconds=10)],
    )
    req_self_sunlit: Optional[bool] = Field(
        None,
        description="Required instrument sunlit state for valid observation "
        + "(`True`: sunlit, `False`: eclipse, `None`: no requirement).",
    )
    req_target_sunlit: Optional[bool] = Field(
        None,
        description="Required target sunlit state for valid observation "
        + "(`True`: sunlit, `False`: eclipse, `None`: no requirement).",
    )
    access_time_fixed: bool = Field(
        False, description="`True`, if access time is fixed to minimum value."
    )

# -*- coding: utf-8 -*-
"""
Object schemas for satellites.

@author: Paul T. Grogan <paul.grogan@asu.edu>
"""
from datetime import timedelta
from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Literal

from .instrument import Instrument
from .orbit import TwoLineElements, CircularOrbit, SunSynchronousOrbit, KeplerianOrbit


class SpaceSystem(BaseModel):
    """
    Base class for space systems.
    """

    name: str = Field(
        ...,
        description="Space system name.",
        examples=["International Space Station"],
    )
    orbit: Union[
        TwoLineElements, CircularOrbit, SunSynchronousOrbit, KeplerianOrbit
    ] = Field(..., description="Orbit specification.")
    instruments: List[Instrument] = Field(
        [], description="List of assigned instruments."
    )


class Satellite(SpaceSystem):
    """
    Single satellite.
    """

    type: Literal["satellite"] = Field(
        "satellite", description="Space system type discriminator."
    )


class TrainConstellation(Satellite):
    """
    A constellation that arranges member satellites in sequence.
    """

    type: Literal["train"] = Field(
        "train", description="Space system type discriminator."
    )
    orbit: Union[
        TwoLineElements, SunSynchronousOrbit, CircularOrbit, KeplerianOrbit
    ] = Field(..., description="Lead orbit for this constellation.")
    number_satellites: int = Field(
        1, description="The count of the number of satellites.", ge=1
    )
    interval: timedelta = Field(
        ...,
        description="The local time interval between satellites in a train constellation.",
    )
    repeat_ground_track: bool = Field(
        True,
        description="True, if the train satellites should repeat the same ground track.",
    )


class WalkerConfiguration(str, Enum):
    """
    Enumeration of different Walker constellation configurations.
    """

    DELTA = "delta"
    STAR = "star"


class WalkerConstellation(Satellite):
    """
    A constellation that arranges member satellites following the Walker pattern.
    """

    type: Literal["walker"] = Field(
        "walker", description="Space system type discriminator."
    )
    configuration: WalkerConfiguration = Field(
        WalkerConfiguration.DELTA, description="Walker configuration."
    )
    orbit: Union[
        TwoLineElements, SunSynchronousOrbit, CircularOrbit, KeplerianOrbit
    ] = Field(..., description="Lead orbit for this constellation.")
    number_satellites: int = Field(
        1, description="Number of satellites in the constellation.", ge=1
    )
    number_planes: int = Field(
        1,
        description="The number of equally-spaced planes in a Walker Delta "
        + "constellation. Ranges from 1 to (number of satellites).",
        ge=1,
    )
    relative_spacing: int = Field(
        0,
        description="Relative spacing of satellites between plans for a Walker Delta "
        + "constellation. Ranges from 0 for equal true anomaly to "
        + "(number of planes) - 1. For example, `relative_spacing=1` "
        + "means the true anomaly is shifted by `360/number_satellites` "
        + "between adjacent planes.",
        ge=0,
    )

    @model_validator(mode="after")
    def number_planes_le_number_satellites(self) -> "WalkerConstellation":
        """
        Validates the number of planes given the number of satellites.
        """
        if (
            self.number_planes is not None
            and self.number_satellites is not None
            and self.number_planes > self.number_satellites
        ):
            raise ValueError("number planes exceeds number satellites")
        return self

    @model_validator(mode="after")
    def relative_spacing_lt_number_planes(self) -> "WalkerConstellation":
        """
        Validates the relative spacing given the number of planes.
        """
        if (
            self.relative_spacing is not None
            and self.number_planes is not None
            and self.relative_spacing >= self.number_planes
        ):
            raise ValueError("relative spacing exceeds number planes - 1")
        return self


class MOGConstellation(Satellite):
    """
    A constellation that arranges member satellites following the mutual orbiting group pattern.

    Based on Stephen Leroy, Riley Fitzgerald, Kerri Cahoy, James Abel, and James Clark (2020).
    "Orbital Maintenance of a Constellation of CubeSats for Internal Gravity Wave Tomography,"
    IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, vol. 13,
    pp. 307-317. doi: 10.1109/JSTARS.2019.2961084
    """

    type: Literal["mog"] = Field("mog", description="Space system type discriminator.")
    orbit: CircularOrbit = Field(
        ..., description="Reference circular orbit for this constellation."
    )
    parallel_axis: float = Field(
        ...,
        description="Mutual orbit axis length (m) parallel to velocity vector.",
        gt=0,
    )
    transverse_axis: float = Field(
        ...,
        description="Mutual orbit axis length (m) transverse to velocity vector.",
        gt=0,
    )
    clockwise: bool = Field(True, description="True, if the mutual orbit is clockwise.")
    number_satellites: int = Field(
        2, description="Number of equally-spaced mutually orbiting satellites.", gt=0
    )

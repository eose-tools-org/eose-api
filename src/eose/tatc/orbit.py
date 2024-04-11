# -*- coding: utf-8 -*-
"""
Object schemas for satellite orbits.

@author: Paul T. Grogan <paul.grogan@asu.edu>
"""

from datetime import datetime, time, timezone
from typing import List, Optional
import re

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Literal


class TwoLineElements(BaseModel):
    """
    Orbit defined with standard two line elements.
    """

    type: Literal["tle"] = Field("tle", description="Orbit type discriminator.")
    tle: List[str] = Field(
        ...,
        description="Two line elements.",
        min_length=2,
        max_length=2,
        examples=[
            [
                "1 25544U 98067A   21156.30527927  .00003432  00000-0  70541-4 0  9993",
                "2 25544  51.6455  41.4969 0003508  68.0432  78.3395 15.48957534286754",
            ]
        ],
    )

    @field_validator("tle")
    @classmethod
    def valid_tle(cls, v):
        """
        Validate the two line element set.
        """
        # based on orekit's TLE.isFormatOK function
        if len(v[0]) != 69:
            raise ValueError("Invalid tle: line 1 incorrect length.")
        if len(v[1]) != 69:
            raise ValueError("Invalid tle: line 2 incorrect length.")

        line_1_pattern = (
            r"1 [ 0-9A-HJ-NP-Z][ 0-9]{4}[A-Z] [ 0-9]{5}[ A-Z]{3} "
            + r"[ 0-9]{5}[.][ 0-9]{8} (?:(?:[ 0+-][.][ 0-9]{8})|(?: "
            + r"[ +-][.][ 0-9]{7})) [ +-][ 0-9]{5}[+-][ 0-9] "
            + r"[ +-][ 0-9]{5}[+-][ 0-9] [ 0-9] [ 0-9]{4}[ 0-9]"
        )
        if re.match(line_1_pattern, v[0]) is None:
            raise ValueError("Invalid tle: line 1 does not match pattern.")
        line_2_pattern = (
            r"2 [ 0-9A-HJ-NP-Z][ 0-9]{4} [ 0-9]{3}[.][ 0-9]{4} "
            + r"[ 0-9]{3}[.][ 0-9]{4} [ 0-9]{7} [ 0-9]{3}[.][ 0-9]{4} "
            + r"[ 0-9]{3}[.][ 0-9]{4} [ 0-9]{2}[.][ 0-9]{13}[ 0-9]"
        )
        if re.match(line_2_pattern, v[1]) is None:
            raise ValueError("Invalid tle: line 2 does not match pattern.")

        def checksum(line):
            the_sum = 0
            for i in range(68):
                if line[i].isdigit():
                    the_sum += int(line[i])
                elif line[i] == "-":
                    the_sum += 1
            return the_sum % 10

        if int(v[0][68]) != checksum(v[0]):
            raise ValueError("Invalid tle: line 1 checksum failed.")
        if int(v[1][68]) != checksum(v[1]):
            raise ValueError("Invalid tle: line 2 checksum failed.")
        return v


class OrbitBase(BaseModel):
    """
    Base class for orbits.
    """

    altitude: float = Field(..., description="Mean altitude (meters).")
    true_anomaly: float = Field(0, description="True anomaly (degrees).", ge=0, lt=360)
    epoch: Optional[datetime] = Field(
        datetime.now(tz=timezone.utc),
        description="Timestamp (epoch) of the initial orbital state.",
    )


class CircularOrbit(OrbitBase):
    """
    Orbit specification using Keplerian elements for elliptical motion -- circular motion case.
    """

    type: Literal["circular"] = Field(
        "circular", description="Orbit type discriminator."
    )
    inclination: float = Field(0, description="Inclination (degrees).", ge=0, lt=180)
    right_ascension_ascending_node: float = Field(
        0, description="Right ascension of ascending node (degrees).", ge=0, lt=360
    )


class SunSynchronousOrbit(OrbitBase):
    """
    Orbit defined by sun synchronous parameters.
    """

    type: Literal["sso"] = Field("sso", description="Orbit type discriminator.")
    altitude: float = Field(
        ...,
        description="Mean altitude (meters).",
        ge=0,
        lt=5980991.22858,
    )
    equator_crossing_time: time = Field(
        ..., description="Equator crossing time (local solar time)."
    )
    equator_crossing_ascending: bool = Field(
        True,
        description="True, if the equator crossing time is ascending (south-to-north).",
    )


class KeplerianOrbit(CircularOrbit):
    """
    Orbit specification using Keplerian elements for elliptical motion.
    """

    type: Literal["keplerian"] = Field(
        "keplerian", description="Orbit type discriminator."
    )
    eccentricity: float = Field(0, description="Eccentricity.", ge=0)
    perigee_argument: float = Field(
        0, description="Perigee argument (degrees).", ge=0, lt=360
    )

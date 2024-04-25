"""
Utility data types.
"""

from typing import Literal, Union

from pydantic import StrictInt, StrictStr

CoordinateReferenceSystem = Literal[
    "EPSG:4326",  # Earth WGS 1984
    "ESRI:104902",  # Venus 2000
    "ESRI:104903",  # Moon 2000
    "ESRI:104905",  # Mars 2000
    "ESRI:104975",  # Sun IAU 2015
]
Identifier = Union[StrictInt, StrictStr]

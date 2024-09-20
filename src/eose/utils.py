"""
Utility data types.
"""

from enum import Enum
from typing import List, Union
from typing_extensions import Annotated

from pydantic import Field, StrictInt, StrictStr

Identifier = Union[StrictInt, StrictStr]

Vector = Annotated[
    List[float],
    Field(min_length=3, ma_length=3, description="Cartesian vector (x,y,z)."),
]

Quaternion = Annotated[
    List[float],
    Field(min_length=4, max_length=4, description="Quaternion (x,y,z,w)."),
]


class PlanetaryCoordinateReferenceSystem(str, Enum):
    EPSG_4326 = "EPSG:4326"  # Earth WGS 1984
    ESRI_104902 = "ESRI:104902"  # Venus 2000
    ESRI_104903 = "ESRI:104903"  # Moon 2000
    ESRI_104905 = "ESRI:104905"  # Mars 2000
    ESRI_104975 = "ESRI:104975"  # Sun IAU 2015


class CartesianReferenceFrame(str, Enum):
    ITRS = "ITRS"  # International Terrestrial Reference System (ITRS)
    ICRF = "ICRF"  # International Celestial Reference Frame


class FixedOrientation(str, Enum):
    """
        The axis of the Nadir-pointing reference frame are defined as follows:

        * :math:`\bf X_{np}` axis: :math:`-({\bf Z_{np}} \times {\bf V})`, where :math:`\bf V` is the Velocity vector of satellite in EARTH_FIXED frame
                
        * :math:`\bf Y_{np}` axis: :math:`({\bf Z_{np}} \times {\bf X_{np}})`
                
        * :math:`\bf Z_{np}` axis: Aligned to Nadir vector (i.e. the negative of the position vector of satellite in case of the `NADIR_GEOCENTRIC`.)
    
        (Note that this results in roll axis as `Y_{np}` and not `X_{np}`.)
        
    """
    NADIR_GEOCENTRIC = "NADIR_GEOCENTRIC"  # nadir pointing through geocenter
    NADIR_GEODETIC = "NADIR_GEODETIC"  # nadir normal to ellipsoid surface


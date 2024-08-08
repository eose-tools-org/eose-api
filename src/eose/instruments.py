from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, model_validator
from enum import Enum

# Ensure the import path for Quaternion is correct
from eose.utils import Quaternion

class CircularGeometry(BaseModel):
    """Class to handle spherical circular geometries which define a closed angular space of interest.
       The pointing axis is fixed to the sensor Z-axis. 
    """
    type: Literal["CircularGeometry"] = Field("CircularGeometry")
    diameter: float = Field(..., gt=0, lt=180, description="Angular diameter of circular geometry about the sensor Z-axis in degrees.")

class RectangularGeometry(BaseModel):
    """Class to handle spherical rectangular geometries which define a closed angular space of interest.
       The pointing axis is fixed to the sensor Z-axis. 
    """
    type: Literal["RectangularGeometry"] = Field("RectangularGeometry")
    angle_height: Optional[float] = Field(None, gt=0, lt=180, description="Angular height (about the sensor X-axis) of the rectangular geometry in degrees.")
    angle_width: Optional[float] = Field(None, gt=0, lt=180, description="Angular width (about the sensor Y-axis) of the rectangular geometry in degrees.")

class BasicSensor(BaseModel):
    name: Optional[str] = Field(None, description="Sensor name.")
    id: Optional[str] = Field(None, description="Sensor identifier.")
    mass: Optional[float] = Field(None, gt=0, description="Mass of the sensor in kilograms.")
    volume: Optional[float] = Field(None, gt=0, description="Volume of the sensor in cubic meters.")
    power: Optional[float] = Field(None, gt=0, description="(Average) Power consumption of the sensor in watts.")
    orientation: Quaternion = Field(
        default_factory=lambda: list([0, 0, 0, 1]),
        description="Orientation of the instrument view, relative to the spacecraft body-fixed frame.",
    )
    field_of_view: Union[CircularGeometry, RectangularGeometry] = Field(
        default_factory=lambda: CircularGeometry(diameter=30), 
        description="Field of view of the sensor."
    )
    data_rate: Optional[float] = Field(None, gt=0, description="Data rate of the sensor in megabits per second.")
    bits_per_pixel: Optional[int] = Field(None, gt=1, description="Bits per pixel for the sensor's data output.")





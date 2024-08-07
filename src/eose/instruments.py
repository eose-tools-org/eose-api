from typing import Optional
from pydantic import BaseModel, Field, model_validator
from enum import Enum

# Ensure the import path for Quaternion is correct
from eose.utils import Quaternion

class Shape(str, Enum):
    CIRCULAR = "CIRCULAR"
    RECTANGULAR = "RECTANGULAR"

class SphericalGeometry(BaseModel):
    """Class to handle spherical geometries (spherical circle or rectangular) which define a closed angular space of interest.
       The pointing axis is fixed to the sensor Z-axis. 
    """
    shape: Shape = Field(Shape.CIRCULAR, description="Shape of the spherical geometry.")
    diameter: Optional[float] = Field(None, gt=0, lt=180, description="Angular diameter of circular geometry about the sensor Z-axis in degrees.")
    angle_height: Optional[float] = Field(None, gt=0, lt=180, description="Angular height (about the sensor X-axis) of the rectangular geometry in degrees.")
    angle_width: Optional[float] = Field(None, gt=0, lt=180, description="Angular width (about the sensor Y-axis) of the rectangular geometry in degrees.")
    
    class Config:
        use_enum_values = True  # This will make the enum values used directly instead of their names

    @model_validator(mode='before')
    def check_geometry_consistency(cls, values):
        shape = values.get('shape')
        diameter = values.get('diameter')
        angle_height = values.get('angle_height')
        angle_width = values.get('angle_width')
        
        if shape == Shape.CIRCULAR:
            if diameter is None:
                raise ValueError('CIRCULAR shape must have a diameter.')
            if angle_height is not None or angle_width is not None:
                raise ValueError('CIRCULAR shape cannot have angle_height or angle_width.')

        elif shape == Shape.RECTANGULAR:
            if angle_height is None or angle_width is None:
                raise ValueError('RECTANGULAR shape must have both angle_height and angle_width.')
            if diameter is not None:
                raise ValueError('RECTANGULAR shape cannot have a diameter.')

        return values

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
    field_of_view: SphericalGeometry = Field(
        default_factory=lambda: SphericalGeometry(diameter=30), 
        description="Field of view of the sensor."
    )
    data_rate: Optional[float] = Field(None, gt=0, description="Data rate of the sensor in megabits per second.")
    bits_per_pixel: Optional[int] = Field(None, gt=1, description="Bits per pixel for the sensor's data output.")





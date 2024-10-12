from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, model_validator
from enum import Enum

from eose.utils import Quaternion


class CircularGeometry(BaseModel):
    """Class to handle spherical circular geometries which define a closed angular space of interest.
    The pointing axis is fixed to the sensor Z-axis.
    """

    type: Literal["CircularGeometry"] = Field("CircularGeometry")
    diameter: float = Field(
        ...,
        gt=0,
        lt=180,
        description="Angular diameter of circular geometry about the sensor Z-axis in degrees.",
    )

class RectangularGeometry(BaseModel):
    """Class to handle spherical rectangular geometries which define a closed angular space of interest.
    The pointing axis is fixed to the sensor Z-axis.
    """

    type: Literal["RectangularGeometry"] = Field("RectangularGeometry")
    angle_height: Optional[float] = Field(
        None,
        gt=0,
        lt=180,
        description="Angular height (about the sensor X-axis) of the rectangular geometry in degrees.",
    )
    angle_width: Optional[float] = Field(
        None,
        gt=0,
        lt=180,
        description="Angular width (about the sensor Y-axis) of the rectangular geometry in degrees.",
    )

class BasicSensor(BaseModel):
    type: Literal["BasicSensor"] = Field("BasicSensor")
    name: Optional[str] = Field(None, description="Sensor name.")
    id: Optional[str] = Field(None, description="Sensor identifier.")
    mass: Optional[float] = Field(
        None, gt=0, description="Mass of the sensor in kilograms."
    )
    volume: Optional[float] = Field(
        None, gt=0, description="Volume of the sensor in cubic centimeter."
    )
    power: Optional[float] = Field(
        None, gt=0, description="(Average) Power consumption of the sensor in watts."
    )
    orientation: Quaternion = Field(
        default_factory=lambda: list([0, 0, 0, 1]),
        description="Orientation of the sensor body-fixed frame, relative to the spacecraft body-fixed frame. It is assumed that the sensor field of view (FOV) is aligned to the sensor body-fixed frame, and the sensor's FOV axis is aligned with its z-axis.",
    )
    field_of_view: Union[CircularGeometry, RectangularGeometry] = Field(
        default_factory=lambda: CircularGeometry(diameter=30),
        description="Field of view of the sensor.",
    )
    data_rate: Optional[float] = Field(
        None, gt=0, description="Data rate of the sensor in megabits per second."
    )
    bits_per_pixel: Optional[int] = Field(
        None, ge=1, description="Bits per pixel for the sensor's data output."
    )

class ScanTechnique(str, Enum):
    PUSHBROOM = "PUSHBROOM"
    WHISKBROOM = "WHISKBROOM"
    MATRIX_IMAGER = "MATRIX_IMAGER"

class PassiveOpticalScanner(BaseModel):
    type: Literal["PassiveOpticalScanner"] = Field("PassiveOpticalScanner")
    name: Optional[str] = Field(None, description="Sensor name.")
    id: Optional[str] = Field(None, description="Sensor identifier.")
    mass: Optional[float] = Field(
        None, gt=0, description="Mass of the sensor in kilograms."
    )
    volume: Optional[float] = Field(
        None, gt=0, description="Volume of the sensor in cubic centimeter."
    )
    power: Optional[float] = Field(
        None, gt=0, description="(Average) Power consumption of the sensor in watts."
    )
    orientation: Quaternion = Field(
        default_factory=lambda: list([0, 0, 0, 1]),
        description="Orientation of the sensor body-fixed frame, relative to the spacecraft body-fixed frame. It is assumed that the sensor field of view (FOV) is aligned to the sensor body-fixed frame, and the sensor's FOV axis is aligned with its z-axis.",
    )
    field_of_view: Union[CircularGeometry, RectangularGeometry] = Field(
        default_factory=lambda: CircularGeometry(diameter=30),
        description="Field of view of the sensor."
    )
    scene_field_of_view: Union[CircularGeometry, RectangularGeometry] = Field(
        default_factory=lambda: CircularGeometry(diameter=30),
        description="Scene field of view of the sensor."
    )
    data_rate: Optional[float] = Field(
        None, gt=0, description="Data rate of the sensor in megabits per second."
    )
    scan_technique: Union[ScanTechnique, str] = Field(
        ScanTechnique.MATRIX_IMAGER,
        description="Scan technique"
    )
    number_detector_rows: Optional[int] = Field(
        None, ge=1, description="Number of detector rows (along the Y-axis of the sensor body-fixed frame). If the sensor body-fixed frame is aligned to the nadir-pointing frame, then this direction corresponds to the along-track direction."
    )
    number_detector_cols: Optional[int] = Field(
        None, ge=1, description="Number of detector columns (along the X-axis of the sensor body-fixed frame). If the sensor body-fixed frame is aligned to the nadir-pointing frame, then this direction corresponds to the cross-track direction."
    )
    aperture_dia: float = Field(
        None, ge=0, description="Telescope aperture diameter in meters."
    )
    F_num: float = Field(
        None, gt=0, description="F-number/ F# of lens."
    )
    focal_length: float = Field(
        None, gt=0, description="Focal length of lens in meters."
    )
    operating_wavelength: float = Field(
        None, gt=0, description="Center operating wavelength in meters."
    )
    bandwidth: float = Field(
        None, gt=0, description="Bandwidth of operation in meters. It is assumed that the detector element supports the entire bandwidth with same quantum efficiency for all wavelengths. Assumption maybe reasonable for narrow-bandwidths."
    )
    quantum_efficiency: float = Field(
        None, ge=0, le=1, description="Quantum efficiency of the detector element."
    )
    optics_sys_eff: Optional[float] = Field(
        1, gt=0, le=1, description="Optical systems efficiency."
    )
    number_of_read_out_E: float = Field(
        None, ge=0, description="Number of read out electrons of the detector."
    )
    target_black_body_temp: float = Field(
        None, ge=0, description="Target body's equivalent black-body temperature in Kelvin."
    )
    bits_per_pixel: Optional[int] = Field(
        None, ge=1, description="Bits per pixel for the sensor's data output."
    )
    detector_width: float = Field(
        None, ge=0, description="Width of detector element in meters."
    )
    max_detector_exposure_time: Optional[float] = Field(
        None, ge=0, description="Maximum exposure time of detector in seconds."
    )

class SyntheticApertureRadar(BaseModel):
    type: Literal["SyntheticApertureRadar"] = Field("SyntheticApertureRadar")

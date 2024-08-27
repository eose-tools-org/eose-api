from typing import List, Optional, Literal, Union
from datetime import timedelta

from geopandas import GeoDataFrame
from pandas import to_timedelta
from pydantic import AwareDatetime, BaseModel, Field

from .geometry import Point, Feature
from .targets import TargetPoint
from .instruments import BasicSensor, PassiveOpticalScanner, SyntheticApertureRadar
from .propagation import PropagationRecord, PropagationResponse
from .coverage import CoverageSample, CoverageRecord, CoverageResponse

class DataMetricRequest(BaseModel):
    """ The data-metrics are calculated for all the target points within the coverage response.
    """
    sensor: Union[BasicSensor, PassiveOpticalScanner, SyntheticApertureRadar] = Field(..., description="Specifications of the sensor.")
    start: AwareDatetime = Field(..., description="Data metrics analysis start time.")
    duration: timedelta = Field(..., ge=0, description="Data metrics analysis duration.")
    #targets: List[TargetPoint] = Field(..., description="Target points.")
    propagation_response: List[PropagationResponse] = Field(..., description="Satellite states during the requested analysis period.")
    coverage_response: List[CoverageResponse] = Field(..., description="Coverage during the requested analysis period.")

class BasicSensorDataMetricInstantaneous(BaseModel):
    """ Basic sensor data metrics results calculated at an instant."""
    type: Literal["BasicSensor"] = Field("BasicSensor")
    time: AwareDatetime = Field(..., description="Time instant at which the data metrics are recorded.")
    incidence_angle: float = Field(..., description="Incidence angle in degrees at the target point calculated assuming spherical Earth.")
    look_angle: float = Field(..., description=" Look angle in degrees at the target point calculated assuming spherical Earth. Positive sign => look is in positive half-space made by the orbit-plane (i.e. orbit plane normal vector) and vice-versa.")
    observation_range: float = Field(..., description="Distance in kilometers from satellite to ground-point during the observation.")
    solar_zenith: float = Field(..., description="Solar Zenith angle in degrees during observation.")

class BasicSensorDataMetricSample(BaseModel):
    """ Aggregation of data metrics per overpass (for a target). """
    type: Literal["BasicSensor"] = Field("BasicSensor")
    instantaneous_metrics: List[BasicSensorDataMetricInstantaneous] = Field([], description="List of instantaneous data metrics calculated during a single overpass.")
    
class BasicSensorDataMetricRecord(BaseModel):
    """ Aggregation of data metrics per target (across possibly *multiple* overpasses). """
    type: Literal["BasicSensor"] = Field("BasicSensor")
    target: TargetPoint = Field(..., description="Target point.")
    samples: List[BasicSensorDataMetricSample] = Field([], description="List of data metric samples.")
    
class BasicSensorDataMetricResponse(BaseModel):
    """ Aggregation of data metrics over all targets (and all overpasses). """
    type: Literal["BasicSensor"] = Field("BasicSensor")
    records: List[BasicSensorDataMetricRecord] = Field([], description="List of data metrics records.")


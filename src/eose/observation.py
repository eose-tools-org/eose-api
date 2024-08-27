from typing import List
from datetime import timedelta

from geopandas import GeoDataFrame
from pydantic import AwareDatetime, BaseModel, Field

from .geometry import Point, Feature, FeatureCollection
from .targets import TargetPoint
from .satellites import Satellite


class ObservationRequest(BaseModel):
    start: AwareDatetime = Field(..., description="Observation analysis start time.")
    duration: timedelta = Field(..., ge=0, description="Observation analysis duration.")
    targets: List[TargetPoint] = Field(..., description="Target points.")
    satellites: List[Satellite] = Field(..., description="Member satellites.")


class ObservationSample(BaseModel):
    source: str = Field(None, description="Source of sample observation.")
    start: AwareDatetime = Field(..., description="Observation sample start time.")
    duration: timedelta = Field(..., ge=0, description="Observation sample duration.")


class ObservationRecord(BaseModel):
    target: TargetPoint = Field(..., description="Target point.")
    samples: List[ObservationSample] = Field(
        [], description="List of observation samples."
    )

    def as_feature(self) -> Feature:
        """
        Convert this observation record to a GeoJSON `Feature`.
        """
        return Feature(
            type="Feature",
            geometry=self.as_geometry(),
            properties=self.model_dump(),
        )

    def as_geometry(self) -> Point:
        """
        Convert this observation record to a GeoJSON `Point` geometry.
        """
        return self.target.as_geometry()


class ObservationResponse(ObservationRequest):
    observations: List[ObservationRecord] = Field([], description="Observation results")

    def as_features(self) -> FeatureCollection:
        """
        Converts this observation response to a GeoJSON `FeatureCollection`.
        """
        return FeatureCollection(
            type="FeatureCollection",
            features=[record.as_feature() for record in self.observations],
        )

    def as_dataframe(self) -> GeoDataFrame:
        """
        Converts this observation response to a `geopandas.GeoDataFrame`.
        """
        gdf = GeoDataFrame.from_features(self.as_features())
        return gdf

from typing import List
from datetime import timedelta

from geopandas import GeoDataFrame
from pandas import to_timedelta
from pydantic import AwareDatetime, BaseModel, Field

from .base import BaseRequest
from .geometry import Point, Feature, FeatureCollection
from .targets import TargetPoint
from .utils import Identifier


class ObservationRequest(BaseRequest):
    targets: List[TargetPoint] = Field(..., description="Target points.")
    instrument_ids: List[Identifier] = Field(
        ..., description="List of instrument identifiers to consider for analysis."
    )


class ObservationSample(BaseModel):
    satellite_id: str = Field(None, description="ID of satellite making observation.")
    instrument_id: str = Field(None, description="ID of instrument making observation.")
    start: AwareDatetime = Field(..., description="Observation sample start time.")
    duration: timedelta = Field(..., ge=0, description="Observation sample duration.")

    def as_feature(self, target: TargetPoint) -> Feature:
        """
        Convert this observation sample to a GeoJSON `Feature`.
        """
        return Feature(
            type="Feature",
            geometry=target.as_geometry(),
            properties=dict({"target_id": target.id}, **self.model_dump()),
        )


class ObservationRecord(BaseModel):
    target_id: Identifier = Field(..., description="Target point identifier.")
    samples: List[ObservationSample] = Field(
        [], description="List of observation samples."
    )

    def as_feature(self, target: TargetPoint) -> Feature:
        """
        Convert this observation record to a GeoJSON `Feature`.
        """
        return Feature(
            type="Feature",
            geometry=self.as_geometry(target),
            properties=self.model_dump(),
        )

    def as_geometry(self, target: TargetPoint) -> Point:
        """
        Convert this observation record to a GeoJSON `Point` geometry.
        """
        return target.as_geometry()


class ObservationResponse(ObservationRequest):
    target_records: List[ObservationRecord] = Field(
        [], description="Observation results"
    )

    def as_features(self) -> FeatureCollection:
        """
        Converts this observation response to a GeoJSON `FeatureCollection`.
        """
        return FeatureCollection(
            type="FeatureCollection",
            features=[
                sample.as_feature(
                    next(
                        target
                        for target in self.targets
                        if target.id == record.target_id
                    )
                )
                for record in self.target_records
                for sample in record.samples
            ],
        )

    def as_dataframe(self) -> GeoDataFrame:
        """
        Converts this observation response to a `geopandas.GeoDataFrame`.
        """
        gdf = GeoDataFrame.from_features(self.as_features())
        gdf["duration"] = to_timedelta(gdf["duration"])  # helper for type coersion
        return gdf

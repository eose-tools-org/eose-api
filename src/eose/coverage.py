from typing import List, Optional
from datetime import timedelta

from geopandas import GeoDataFrame
from pandas import to_timedelta
from pydantic import Field

from .geometry import FeatureCollection
from .observation import ObservationSample, ObservationRecord, ObservationResponse


class CoverageRequest(ObservationResponse):
    pass


class CoverageSample(ObservationSample):
    revisit: Optional[timedelta] = Field(
        None, ge=0, description="Elapsed time since prior observation."
    )


class CoverageRecord(ObservationRecord):
    samples: List[ObservationSample] = Field(
        [], description="List of observation samples."
    )
    mean_revisit: Optional[timedelta] = Field(
        None,
        ge=0,
        description="Mean elapsed time between observations.",
    )
    number_samples: int = Field(0, ge=0, description="Number of observation samples.")


class CoverageResponse(CoverageRequest):
    target_records: List[CoverageRecord] = Field([], description="Coverage results.")
    harmonic_mean_revisit: Optional[timedelta] = Field(
        None, ge=0, description="Harmonic mean revisit time over all targets."
    )
    coverage_fraction: float = Field(
        0, ge=0, le=1, description="Fraction of targets observed at least once."
    )

    def as_features(self) -> FeatureCollection:
        """
        Converts this coverage response to a GeoJSON `FeatureCollection`.
        """
        return FeatureCollection(
            type="FeatureCollection",
            features=[
                record.as_feature(
                    next(
                        target
                        for target in self.targets
                        if target.id == record.target_id
                    )
                )
                for record in self.target_records
            ],
        )

    def as_dataframe(self) -> GeoDataFrame:
        """
        Converts this coverage response to a `geopandas.GeoDataFrame`.
        """
        gdf = GeoDataFrame.from_features(self.as_features())
        gdf["mean_revisit"] = to_timedelta(
            gdf["mean_revisit"]
        )  # helper for type coersion
        return gdf

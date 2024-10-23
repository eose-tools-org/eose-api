from typing import List, Optional
from datetime import timedelta

from geopandas import GeoDataFrame
from pandas import to_timedelta
from pydantic import Field

from .geometry import FeatureCollection
from .access import AccessSample, AccessRecord, AccessResponse
from .utils import Identifier


class CoverageRequest(AccessResponse):
    omit_payload_ids: List[Identifier] = Field(
        [], description="List of payload identifiers to omit from analysis."
    )
    omit_satellite_ids: List[Identifier] = Field(
        [], description="List of satellite identifiers to omit from analysis."
    )


class CoverageSample(AccessSample):
    revisit: Optional[timedelta] = Field(
        None, ge=0, description="Elapsed time since prior access."
    )


class CoverageRecord(AccessRecord):
    samples: List[CoverageSample] = Field([], description="List of coverage samples.")
    mean_revisit: Optional[timedelta] = Field(
        None,
        ge=0,
        description="Mean elapsed time between accesses.",
    )
    number_samples: int = Field(0, ge=0, description="Number of access samples.")


class CoverageResponse(CoverageRequest):
    target_records: List[CoverageRecord] = Field([], description="Coverage results.")
    harmonic_mean_revisit: Optional[timedelta] = Field(
        None, ge=0, description="Harmonic mean revisit time over all targets."
    )
    coverage_fraction: float = Field(
        0, ge=0, le=1, description="Fraction of targets accessed at least once."
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

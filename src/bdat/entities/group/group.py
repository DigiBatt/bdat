import typing
from dataclasses import dataclass, field

from bson import ObjectId

import bdat.entities as entities
from bdat.entities.data_processing import DataProcessing


@dataclass
class Group(DataProcessing):
    id: ObjectId | None = field(init=False)
    collection_id: str | None = None
    testset: "entities.ActivitySet | None" = None
    project: "entities.Project | None" = None
    species: "entities.BatterySpecies | None" = None
    specimen: "entities.Battery | None" = None
    test: "entities.Cycling | None" = None
    unique: str | None = None
    unique_link: typing.Tuple[str, ...] | None = None
    unique_key: typing.Tuple[str, ...] | None = None
    filter: typing.Tuple[str, ...] | None = None
    exclude_tests: typing.Tuple[str, ...] | None = None

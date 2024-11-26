from dataclasses import dataclass, field
from typing import Any, Dict, List

import pandas as pd
from bson import ObjectId

import altair as alt
from bdat.database.storage.entity import Entity, Filetype, file, identifier
from bdat.entities.data_processing import DataProcessing


@file("data", "plotdata_{key}", Filetype.JSON, explode=True)
@file("plot", "plot", Filetype.JSON)
@identifier("bdat-plot-{plottype}-{resource.id}")
@dataclass
class Plotdata(DataProcessing):
    id: ObjectId | None = field(init=False)
    resource: Entity
    plottype: str
    data: Dict[str, List[Dict]] | Dict[str, pd.DataFrame] = field(default_factory=dict)
    plot: List[Dict] | None = None

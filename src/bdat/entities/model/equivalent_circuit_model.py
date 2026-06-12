import typing
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from bdat.database.storage.entity import Embedded, Filetype, file, identifier
from bdat.entities.cadi_templates import BatterySpecies, Cycling
from bdat.entities.data_processing import DataProcessing
from bdat.entities.patterns.test_eval import TestEval


@dataclass
@file("xml", "model.xml", Filetype.TEXT)
@file("eisplot", "eisplot", Filetype.JSON)
@file("ocvplot", "ocvplot", Filetype.JSON)
@file("modeldata", "modeldata", Filetype.PARQUET)
@identifier("bdat-ecm-{batterySpecies.id}-{lastTest.id}")
class EquivalentCircuitModel(DataProcessing):
    batterySpecies: BatterySpecies
    lastTest: Cycling
    evals: typing.List[TestEval]
    circuit: str
    version: str
    modeldata: pd.DataFrame
    xml: str
    eisplot: typing.Dict
    ocvplot: typing.Dict

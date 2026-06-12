import typing
from dataclasses import dataclass
from datetime import datetime

from bdat.database.storage.entity import Embedded, Filetype, file, identifier
from bdat.entities.cadi_templates import (
    Battery,
    BatterySpecies,
    CyclerCircuit,
    Cycling,
    Entity,
    Project,
)
from bdat.entities.data_processing import DataProcessing
from bdat.entities.model.equivalent_circuit_model import EquivalentCircuitModel


@dataclass
class PlannedTest(Embedded):
    battery: Battery
    circuit: CyclerCircuit
    program: str
    start: datetime
    end: datetime | None
    variables: typing.Dict[str, float]
    requirements: typing.Dict[str, float]
    test: Cycling | None = None


@dataclass
@identifier("bdat-testplan-{title}")
@file("entries", "entries", Filetype.JSON)
class Testplan(DataProcessing):
    entries: typing.List[PlannedTest]
    variables: typing.List[str]
    project: Project
    battery: typing.List[Battery]
    batterySpecies: BatterySpecies
    model: EquivalentCircuitModel | None

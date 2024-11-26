import typing
from dataclasses import dataclass

from bdat.database.storage.entity import Embedded


@dataclass
class AgingConditions(Embedded):
    start: float
    end: float
    chargeCurrent: float | None
    dischargeCurrent: float | None
    dischargePower: float | None
    minVoltage: float | None
    maxVoltage: float | None
    meanVoltage: float | None
    minSoc: float | None
    maxSoc: float | None
    meanSoc: float | None
    dod: float | None
    temperature: float | None

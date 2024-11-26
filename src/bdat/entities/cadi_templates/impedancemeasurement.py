import typing
from dataclasses import dataclass
from datetime import datetime

from . import battery, legalentity, location, tool
from .measurement import Measurement


@dataclass
class ImpedanceMeasurement(Measurement):
    actor: "legalentity.LegalEntity | None"
    tool: "tool.Tool | None"
    location: "location.Location | None"
    object: "battery.Battery"
    time: "datetime | None"
    impedance: "float | None"
    temperature: "float | None"
    voltage: "float | None"

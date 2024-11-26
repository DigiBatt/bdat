import typing
from dataclasses import dataclass
from datetime import datetime

from . import legalentity, location, objectofresearch, tool
from .measurement import Measurement


@dataclass
class WeightMeasurement(Measurement):
    actor: "legalentity.LegalEntity | None"
    tool: "tool.Tool | None"
    location: "location.Location | None"
    object: "objectofresearch.ObjectOfResearch"
    time: "datetime | None"
    weight: "float | None"

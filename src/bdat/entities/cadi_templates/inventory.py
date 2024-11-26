import typing
from dataclasses import dataclass

from . import legalentity, location, measurement, objectofresearch, tool
from .measurement import Measurement


@dataclass
class Inventory(Measurement):
    actor: "legalentity.LegalEntity"
    tool: "tool.Tool | None"
    location: "location.Location | None"
    object: "objectofresearch.ObjectOfResearch"
    measurement: "measurement.Measurement | None"

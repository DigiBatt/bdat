import typing
from dataclasses import dataclass
from datetime import datetime

from . import legalentity, location, objectofresearch, tool
from .measurement import Measurement


@dataclass
class Size(Measurement):
    actor: "legalentity.LegalEntity"
    tool: "tool.Tool | None"
    location: "location.Location | None"
    object: "objectofresearch.ObjectOfResearch"
    time: "datetime | None"
    width: "float | None"
    length: "float | None"
    height: "float | None"
    diameter: "float | None"

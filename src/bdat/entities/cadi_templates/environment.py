import typing
from dataclasses import dataclass
from datetime import datetime

from . import legalentity, location, objectofresearch, tool
from .measurement import Measurement


@dataclass
class Environment(Measurement):
    actor: "legalentity.LegalEntity"
    tool: "tool.Tool | None"
    location: "location.Location | None"
    object: "objectofresearch.ObjectOfResearch | None"
    start: "datetime | None"
    end: "datetime | None"

import typing
from dataclasses import dataclass
from datetime import datetime

from . import (
    activityset,
    environmentmeasurement,
    legalentity,
    location,
    objectofresearch,
    project,
    tool,
)
from .measurement import Measurement


@dataclass
class EnvironmentSection(Measurement):
    actor: "legalentity.LegalEntity | None"
    tool: "tool.Tool | None"
    location: "location.Location | None"
    object: "objectofresearch.ObjectOfResearch"
    environment: "environmentmeasurement.EnvironmentMeasurement | None"
    set: "activityset.ActivitySet | None"
    project: "project.Project | None"
    start: "datetime | None"
    end: "datetime | None"

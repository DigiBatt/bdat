import typing
from dataclasses import dataclass
from datetime import datetime

from . import (
    activityset,
    battery,
    cyclercircuit,
    environmentsection,
    legalentity,
    location,
    project,
)
from .measurement import Measurement


@dataclass
class Cycling(Measurement):
    actor: "legalentity.LegalEntity | None"
    tool: "cyclercircuit.CyclerCircuit | None"
    location: "location.Location | None"
    object: "battery.Battery"
    set: "activityset.ActivitySet | None"
    project: "project.Project | None"
    parent: "Cycling | None"
    environmentSection: "environmentsection.EnvironmentSection | None"
    start: "datetime | None"
    end: "datetime | None"

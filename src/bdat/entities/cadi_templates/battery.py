import typing
from dataclasses import dataclass
from datetime import datetime

from . import batteryspecies, person, project
from .objectofresearch import ObjectOfResearch


@dataclass
class Battery(ObjectOfResearch):
    project: "project.Project | None"
    type: "batteryspecies.BatterySpecies | None"
    inventoryUser: "person.Person | None"
    properties: "typing.Dict[str, typing.Any] | None"
    inventoryDate: "datetime | None"

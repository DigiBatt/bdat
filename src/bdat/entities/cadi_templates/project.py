import typing
from dataclasses import dataclass
from datetime import datetime

from .managemententity import ManagementEntity


@dataclass
class Project(ManagementEntity):
    status: "str | None"
    start: "datetime | None"
    end: "datetime | None"

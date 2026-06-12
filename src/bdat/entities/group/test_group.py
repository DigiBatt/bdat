import typing
from dataclasses import dataclass, field

import bdat.entities as entities
from bdat.database.storage.entity import collections
from bdat.entities.group import Group


@dataclass
@collections("project", "testset")
class TestGroup(Group):
    tests: typing.List["entities.Cycling"] = field(default_factory=list)

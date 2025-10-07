import typing
from dataclasses import dataclass, field
from datetime import datetime

import bdat.entities.patterns.test_eval as test_eval
from bdat.database.storage.entity import Embedded


@dataclass
class PatternEval(Embedded):
    firstStep: int
    lastStep: int
    start: float
    end: float
    age: float | None
    chargeThroughput: float | None
    matchStart: float | None
    matchEnd: float | None
    starttime: datetime | None
    testEval: "test_eval.TestEval | None" = field(init=False, default=None)

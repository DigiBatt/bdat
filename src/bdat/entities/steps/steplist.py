import typing
from dataclasses import dataclass, field
from datetime import datetime

from bson import ObjectId

import bdat.entities as entities
import bdat.entities.steps.step as step
from bdat.database.storage.entity import Filetype, file, identifier
from bdat.entities.data_processing import DataProcessing

if typing.TYPE_CHECKING:
    from bdat.entities.patterns.testinfo_eval import TestinfoEval


@identifier("bdat-steplist-{test.id}")
@file("steps", "steps", Filetype.PICKLE)
@file("plotdata", "plotdata_{key}", Filetype.JSON, explode=True)
@dataclass
class Steplist(DataProcessing):
    """List of steps found in a cycling test."""

    steps: typing.List[step.Step]
    test: "entities.Cycling"
    plotdata: typing.Dict[str, typing.List[typing.Dict]] | None = None

    @typing.overload
    def __getitem__(self, index: int) -> step.Step:
        ...

    @typing.overload
    def __getitem__(self, index: slice) -> typing.List[step.Step]:
        ...

    def __getitem__(self, index: int | slice) -> step.Step | typing.List[step.Step]:
        return self.steps[index]

    def __iter__(self) -> typing.Iterator[step.Step]:
        return self.steps.__iter__()

    def __len__(self):
        return len(self.steps)

    def continue_soc(self, soc: float, capacity: float, first: int = 0):
        for s in self.steps[first:]:
            s.capacity = capacity
            s.socStart = soc
            soc += s.charge / capacity * 100
            s.socEnd = soc

    def continue_counters(self, charge: float, discharge: float, age: float):
        for s in self.steps:
            s.chargeStart = charge
            s.dischargeStart = discharge
            s.ageStart = age
            if s.charge > 0:
                charge += s.charge
            else:
                discharge -= s.charge
            age += s.duration
            s.chargeEnd = charge
            s.dischargeEnd = discharge
            s.ageEnd = age

    def set_time(self, time: float):
        for s in self.steps:
            s.start = time
            time += s.duration
            s.end = time

    def continue_from_counters(
        self,
        charge: float,
        discharge: float,
        age: float,
        date: float,
        soc: float | None,
        capacity: float | None,
    ):
        if len(self.steps) == 0:
            return
        if soc is not None and capacity is not None:
            self.continue_soc(soc, capacity)
        starttime = datetime.timestamp(self.test.start) if self.test.start else 0
        age = age + starttime - date
        self.continue_counters(charge, discharge, age)

    def continue_from_test(self, previous: "TestinfoEval"):
        if previous.lastCharge is None:
            raise Exception("Previous test must have a charge counter")
        if previous.lastDischarge is None:
            raise Exception("Previous test must have a discharge counter")
        if previous.lastAge is None:
            raise Exception("Previous test must have an age counter")
        self.continue_from_counters(
            previous.lastCharge,
            previous.lastDischarge,
            previous.lastAge,
            previous.end,
            previous.lastSoc,
            previous.lastCapacity,
        )

    def continue_from_step(self, previous: step.Step):
        if previous.chargeEnd is None:
            raise Exception("Previous step must have a charge counter")
        if previous.dischargeEnd is None:
            raise Exception("Previous step must have a discharge counter")
        if previous.ageEnd is None:
            raise Exception("Previous step must have an age counter")
        self.continue_from_counters(
            previous.chargeEnd,
            previous.dischargeEnd,
            previous.ageEnd,
            previous.end,
            previous.socEnd,
            previous.capacity,
        )

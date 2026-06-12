import typing
from dataclasses import dataclass, field
from datetime import datetime

import bdat.entities.patterns as patterns
import bdat.entities.steps.step as step
from bdat.database.storage.entity import Filetype, collections, file, identifier
from bdat.entities.cadi_templates import Cycling
from bdat.entities.data_processing import DataProcessing

if typing.TYPE_CHECKING:
    from bdat.entities.patterns.test_eval import TestEval


@identifier("bdat-steplist-{test.id}")
@file("steps", "steps", Filetype.PICKLE)
@file("plotdata", "plotdata_{key}", Filetype.JSON, explode=True)
@collections("test")
@dataclass
class Steplist(DataProcessing):
    """List of steps found in a cycling or EIS test."""

    steps: typing.List[step.Step]
    test: Cycling
    plotdata: typing.Dict[str, typing.List[typing.Dict]] | None = None

    @typing.overload
    def __getitem__(self, index: int) -> step.Step: ...

    @typing.overload
    def __getitem__(self, index: slice) -> typing.List[step.Step]: ...

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

    def set_time(self, time: float):
        for s in self.steps:
            s.start = time
            time += s.duration
            s.end = time

    def continue_from_test(self, test: "Cycling", testinfo: "patterns.TestinfoEval"):
        if testinfo.lastCharge is None:
            raise Exception("Previous test must have a charge counter")
        if testinfo.lastDischarge is None:
            raise Exception("Previous test must have a discharge counter")
        if testinfo.firstAge is None:
            raise Exception("Previous test must have an age counter")
        if test.start is None:
            raise Exception("Previous test must have an end date")
        self.continue_from_counters(
            testinfo.lastCharge,
            testinfo.lastDischarge,
            testinfo.firstAge,
            test.start,
            testinfo.lastSoc,
            testinfo.lastCapacity,
        )

    def rebuild_counters_from_eval(self, testeval: "TestEval"):
        testinfo = None
        captests = []
        for e in testeval.evals:
            if isinstance(e, patterns.TestinfoEval):
                testinfo = e
            elif isinstance(e, patterns.DischargeCapacityEval):
                captests.append(e)

        if testinfo is None:
            raise Exception("Cound not find TestInfo eval")

        if testinfo.firstCharge is None:
            raise Exception("TestInfo must have a charge counter")
        if testinfo.firstDischarge is None:
            raise Exception("TestInfo must have a discharge counter")
        if testinfo.firstAge is None:
            raise Exception("TestInfo must have an age counter")
        if self.test.start is None:
            raise Exception("Test must have a start date")
        self.continue_from_counters(
            testinfo.firstCharge,
            testinfo.firstDischarge,
            testinfo.firstAge,
            self.test.start,
            testinfo.firstSoc,
            testinfo.firstCapacity,
        )

        for e in captests:
            dch_step = self[e.lastStep]
            dch_step.capacity = abs(e.capacity)
            dch_step.socEnd = 0
            if len(self) > dch_step.stepId + 1:
                self.continue_soc(
                    dch_step.socEnd, dch_step.capacity, dch_step.stepId + 1
                )

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

    def continue_from_counters(
        self,
        charge: float,
        discharge: float,
        age: float,
        date: datetime,
        soc: float | None,
        capacity: float | None,
    ):
        if len(self.steps) == 0:
            return
        if soc is not None and capacity is not None:
            self.continue_soc(soc, capacity)
        starttime = datetime.timestamp(self.test.start) if self.test.start else 0
        age = age + starttime - datetime.timestamp(date)
        self.continue_counters(charge, discharge, age)

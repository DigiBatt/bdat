import typing
from dataclasses import dataclass

import pandas as pd

from bdat.entities import BatterySpecies, Cycling
from bdat.entities.patterns import TestinfoEval
from bdat.entities.steps.step import CCStep, CVStep, Step
from bdat.entities.steps.steplist import Steplist
from bdat.entities.test.cycling_data import CyclingData
from bdat.resources.patterns.eval_pattern import EvalPattern
from bdat.steps.step_pattern import StepProperties
from bdat.steps.steplist_pattern import Match, Repeat, SteplistPattern


@dataclass
class Testinfo(EvalPattern):
    def pattern(self, species: BatterySpecies) -> SteplistPattern:
        return Repeat(StepProperties())

    def eval(
        self,
        test: Cycling,
        match: Match,
        steps: typing.List[Step],
        df: CyclingData | None,
    ) -> TestinfoEval:
        return TestinfoEval(
            duration=steps[-1].end - steps[0].start,
            rows=steps[-1].rowEnd,
            chargeAh=sum([max(s.charge, 0) for s in steps]),
            dischargeAh=abs(sum([min(s.charge, 0) for s in steps])),
            totalAh=sum([abs(s.charge) for s in steps]),
            firstVoltage=steps[0].getStartVoltage(),
            lastVoltage=steps[-1].getEndVoltage(),
            minVoltage=min(
                [min(s.getStartVoltage(), s.getEndVoltage()) for s in steps]
            ),
            maxVoltage=max(
                [max(s.getStartVoltage(), s.getEndVoltage()) for s in steps]
            ),
            minCurrent=min(
                [min(s.getStartCurrent(), s.getEndCurrent()) for s in steps]
            ),
            maxCurrent=max(
                [max(s.getStartCurrent(), s.getEndCurrent()) for s in steps]
            ),
            totalStepCount=len(steps),
            CCStepCount=sum([1 if isinstance(s, CCStep) else 0 for s in steps]),
            CVStepCount=sum([1 if isinstance(s, CVStep) else 0 for s in steps]),
            firstStep=0,
            lastStep=steps[-1].stepId,
            start=steps[0].start,
            end=steps[-1].end,
            firstSoc=steps[0].socStart,
            lastSoc=steps[-1].socEnd,
            firstAge=steps[0].ageStart,
            lastAge=steps[-1].ageEnd,
            firstCapacity=steps[0].capacity,
            lastCapacity=steps[-1].capacity,
            firstCharge=steps[0].chargeStart,
            lastCharge=steps[-1].chargeStart,
            firstDischarge=steps[0].dischargeStart,
            lastDischarge=steps[-1].dischargeStart,
            age=steps[0].ageStart,
            chargeThroughput=steps[0].dischargeStart,
        )

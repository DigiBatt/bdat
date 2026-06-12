import datetime
import typing
from dataclasses import dataclass
from typing import Tuple

from bdat.entities import BatterySpecies, Cycling
from bdat.entities.patterns import FullChargeEval
from bdat.entities.steps.step import Step
from bdat.entities.steps.steplist import Steplist
from bdat.entities.test.cycling_data import CyclingData
from bdat.resources.patterns.eval_pattern import EvalPattern
from bdat.steps.step_pattern import CCProperties, CVProperties, PauseProperties
from bdat.steps.steplist_pattern import (
    Match,
    Not,
    Optional,
    Repeat,
    Series,
    SteplistPattern,
)
from bdat.tools.misc import make_range


#: match any full charge so the SOC can be reset to 100%
@dataclass
class FullCharge(EvalPattern):
    eocVoltage: float | Tuple[float, float] | None = None
    chargeCurrent: float | Tuple[float, float] | None = None
    cutoffCurrent: float | Tuple[float, float] | None = None
    ccDuration: float | Tuple[float, float] | None = None
    ccRequired: bool = True
    cvRequired: bool = True

    def pattern(self, species: BatterySpecies) -> SteplistPattern:
        if species.capacity is None:
            raise Exception("Battery species has no defined capacity")
        eocVoltage = make_range(
            [self.eocVoltage, species.endOfChargeVoltage, species.maximumVoltage],
            deltaAbs=(-0.01, 0.02),
        )
        chargeCurrent = make_range(
            [self.chargeCurrent, (0, species.capacity)],
            (0.95, 1.05),
        )
        cutoffCurrent = make_range(
            [self.cutoffCurrent, (0, chargeCurrent[1])], (0.95, 1.05)
        )
        ccDuration = make_range(
            [self.ccDuration, (300, 1e9)], (0.95, 1.05), allowNone=True
        )

        self.chargeStep = CCProperties(
            current=chargeCurrent, voltageEnd=eocVoltage, duration=ccDuration
        )
        self.cvStep = CVProperties(voltage=eocVoltage, currentEnd=cutoffCurrent)

        return Series(
            [
                self.chargeStep if self.ccRequired else Optional(self.chargeStep),
                self.cvStep if self.cvRequired else Optional(self.cvStep),
            ]
        )

    def eval(
        self,
        test: Cycling,
        match: Match,
        steps: typing.List[Step],
        _: CyclingData | None,
    ) -> FullChargeEval:
        chaMatch = next(match.get_matches(self.chargeStep), None)
        chaStep = None if chaMatch is None else chaMatch.steps[0].asCC()
        cvMatch = next(match.get_matches(self.cvStep), None)
        cvStep = None if cvMatch is None else cvMatch.steps[0].asCV()

        firstStep = chaStep or cvStep
        lastStep = cvStep or chaStep

        if firstStep is None or lastStep is None:
            raise Exception()

        return FullChargeEval(
            start=firstStep.start,
            end=lastStep.end,
            firstStep=firstStep.stepId,
            lastStep=lastStep.stepId,
            chargeCurrent=None if chaStep is None else chaStep.current,
            eocVoltage=lastStep.getEndVoltage(),
            ccDuration=None if chaStep is None else chaStep.duration,
            cvDuration=None if cvStep is None else cvStep.duration,
            cutoffCurrent=None if cvStep is None else cvStep.currentEnd,
            age=firstStep.ageStart,
            chargeThroughput=firstStep.dischargeStart,
            matchStart=firstStep.start,
            matchEnd=lastStep.end,
            starttime=(
                test.start + datetime.timedelta(seconds=firstStep.start)
                if test.start
                else None
            ),
        )

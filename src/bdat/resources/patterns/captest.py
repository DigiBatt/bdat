import typing
from dataclasses import dataclass
from typing import Tuple

from bdat.entities import BatterySpecies, Cycling
from bdat.entities.patterns import DischargeCapacityEval
from bdat.entities.steps.step import Step
from bdat.entities.steps.steplist import Steplist
from bdat.entities.test.cycling_data import CyclingData
from bdat.resources.patterns.eval_pattern import EvalPattern
from bdat.steps.step_pattern import CCProperties, CVProperties, PauseProperties
from bdat.steps.steplist_pattern import Match, Optional, Repeat, Series, SteplistPattern
from bdat.tools.misc import make_range


@dataclass
class Captest(EvalPattern):
    eocVoltage: float | Tuple[float, float] | None = None
    eodVoltage: float | Tuple[float, float] | None = None
    chargeCurrent: float | Tuple[float, float] | None = None
    dischargeCurrent: float | Tuple[float, float] | None = None
    cutoffCurrent: float | Tuple[float, float] | None = None
    relaxationTime: float | Tuple[float, float] | None = None
    ccDuration: float | Tuple[float, float] | None = None

    def pattern(self, species: BatterySpecies) -> SteplistPattern:
        if species.capacity is None:
            raise Exception("Battery species has no defined capacity")
        eocVoltage = make_range(
            [self.eocVoltage, species.endOfChargeVoltage, species.maximumVoltage],
            deltaAbs=(-0.01, 0.02),
        )
        eodVoltage = make_range(
            [self.eodVoltage, species.endOfDischargeVoltage, species.minimumVoltage],
            deltaAbs=(-0.05, 0.02),
        )
        chargeCurrent = make_range(
            [self.chargeCurrent, (0, 1e9)],
            (0.95, 1.05),
        )
        dischargeCurrent = make_range(
            [
                self.dischargeCurrent,
                # species.nominalCurrent,
                # species.capacity,
                (-1e9, -0.19 * species.capacity),
            ],
            (-1.05, -0.95),
        )
        cutoffCurrent = make_range(
            [self.cutoffCurrent, (0, chargeCurrent[1])], (0.95, 1.05)
        )
        relaxationTime = make_range([self.relaxationTime, (0, 1e9)], (0.95, 1.05))
        ccDuration = make_range([self.ccDuration], (0.95, 1.05), allowNone=True)

        self.chargeStep = CCProperties(
            current=chargeCurrent, voltageEnd=eocVoltage, duration=ccDuration
        )
        self.cvStep = CVProperties(voltage=eocVoltage, currentEnd=cutoffCurrent)
        self.pauseStep = PauseProperties(duration=relaxationTime)
        self.dischargeStep = CCProperties(
            current=dischargeCurrent, voltageEnd=eodVoltage
        )

        return Series(
            [
                self.chargeStep,
                Optional(self.cvStep),
                self.pauseStep,
                self.dischargeStep,
            ]
        )

    def eval(
        self,
        test: Cycling,
        match: Match,
        steps: typing.List[Step],
        _: CyclingData | None,
    ) -> DischargeCapacityEval:
        chaStep = next(match.get_matches(self.chargeStep)).steps[0].asCC()
        cvMatch = next(match.get_matches(self.cvStep), None)
        cvStep = None if cvMatch is None else cvMatch.steps[0].asCV()
        pauseStep = next(match.get_matches(self.pauseStep)).steps[0].asPause()
        dchStep = next(match.get_matches(self.dischargeStep)).steps[0].asCC()

        capacity = steps[-1].charge
        dischargeCurrent = steps[-1].asCC().current
        dischargeDuration = steps[-1].duration

        # TODO: remove this once all current factors are corrected
        # while abs(capacity) < abs(0.5 * dischargeCurrent * dischargeDuration / 3600):
        #     capacity *= 10
        # while abs(capacity) > abs(2 * dischargeCurrent * dischargeDuration / 3600):
        #     capacity *= 0.1

        return DischargeCapacityEval(
            start=dchStep.start,
            end=dchStep.end,
            firstStep=dchStep.stepId,
            lastStep=dchStep.stepId,
            chargeCurrent=chaStep.current,
            eocVoltage=chaStep.voltageEnd,
            ccDuration=chaStep.duration,
            cvDuration=None if cvStep is None else cvStep.duration,
            cutoffCurrent=None if cvStep is None else cvStep.currentEnd,
            pauseDuration=pauseStep.duration,
            relaxedVoltage=pauseStep.voltageEnd,
            dischargeCurrent=dischargeCurrent,
            dischargeDuration=dischargeDuration,
            capacity=capacity,
            eodVoltage=dchStep.voltageEnd,
            age=dchStep.ageStart,
            chargeThroughput=dchStep.dischargeStart,
        )

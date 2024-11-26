import typing
from dataclasses import dataclass
from typing import Tuple

import numpy as np

from bdat.entities import BatterySpecies, Cycling
from bdat.entities.patterns import PulseEval
from bdat.entities.steps.step import Step
from bdat.entities.steps.steplist import Steplist
from bdat.entities.test.cycling_data import CyclingData
from bdat.resources.patterns.eval_pattern import EvalPattern
from bdat.steps.step_pattern import And, CCProperties, Not, PauseProperties
from bdat.steps.steplist_pattern import Match, Series, SteplistPattern
from bdat.tools.misc import make_range


@dataclass
class Pulse(EvalPattern):
    """Pattern to match a current pulse"""

    #: Current of the pulse in A. If this is a tuple, the current must lie between the two values. If this is a float, a tuple will be constructed by multiplying the value with 0.95 and 1.05.
    current: float | Tuple[float, float] | None = None

    #: Duration of the pulse in seconds. If this is a tuple, the duration must lie between the two values. If this is a float, a tuple will be constructed by multiplying the value with 0.95 and 1.05.
    duration: float | Tuple[float, float] | None = None

    #: Duration of the rest time before the pulse in seconds. If this is a tuple, the duration must lie between the two values. If this is a float, a tuple will be constructed by multiplying the value with 0.95 and 1.05.
    relaxationTime: float | Tuple[float, float] | None = None

    def pattern(self, species: BatterySpecies) -> SteplistPattern:
        current = make_range(
            [self.current, (-1e9, 1e9)],
            (0.95, 1.05),
        )
        duration = make_range([self.duration, (0.5, 60)], (0.95, 1.05))
        relaxationTime = make_range([self.relaxationTime, (600, 1e9)], (0.95, 1.05))

        self.pauseStep = PauseProperties(duration=relaxationTime)
        self.pulseStep = And(
            CCProperties(current=current, duration=duration),
            Not(CCProperties(current=(-0.01, 0.01), duration=duration)),
        )

        return Series([self.pauseStep, self.pulseStep])

    def eval(
        self,
        test: Cycling,
        match: Match,
        steps: typing.List[Step],
        df: CyclingData | None,
    ) -> PulseEval:
        pauseStep = next(match.get_matches(self.pauseStep)).steps[0].asPause()
        pulseStep = next(match.get_matches(self.pulseStep)).steps[0].asCC()

        return PulseEval(
            start=pulseStep.start,
            end=pulseStep.end,
            firstStep=pulseStep.stepId,
            lastStep=pulseStep.stepId,
            relaxationTime=pauseStep.duration,
            current=pulseStep.current,
            duration=pulseStep.duration,
            relaxedVoltage=pauseStep.voltageEnd,
            endVoltage=pulseStep.voltageEnd,
            impedance=(pulseStep.voltageEnd - pauseStep.voltageEnd) / pulseStep.current,
            soc=pulseStep.socStart,
            age=pulseStep.ageStart,
            chargeThroughput=pulseStep.dischargeStart,
        )

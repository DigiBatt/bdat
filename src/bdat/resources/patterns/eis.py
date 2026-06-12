import datetime
import typing
from dataclasses import dataclass

import numpy as np

from bdat.entities import BatterySpecies, Cycling
from bdat.entities.patterns import EISEval
from bdat.entities.steps.step import EISStep, Step
from bdat.entities.test.eis_data import EISData
from bdat.resources.patterns.eval_pattern import EISEvalPattern
from bdat.steps.step_pattern import StepType
from bdat.steps.steplist_pattern import Match, Repeat, SteplistPattern
from bdat.tools.misc import make_range


@dataclass
class EIS(EISEvalPattern):

    def pattern(self, species: BatterySpecies) -> SteplistPattern:
        return Repeat(StepType(stepType=EISStep), min=1)

    def eval(
        self,
        test: Cycling,
        match: Match,
        steps: typing.List[Step],
        _: EISData | None,
    ) -> EISEval:
        return EISEval(
            firstStep=steps[0].stepId,
            lastStep=steps[-1].stepId,
            start=steps[0].start,
            end=steps[-1].end,
            age=steps[0].ageStart,
            chargeThroughput=steps[0].dischargeStart,
            matchStart=steps[0].start,
            matchEnd=steps[-1].end,
            starttime=(
                test.start + datetime.timedelta(seconds=steps[0].start)
                if test.start
                else None
            ),
            batteryVoltage=self.__get_values(steps, "batteryVoltage"),
            frequency=self.__get_values(steps, "frequency"),
            real=self.__get_values(steps, "real"),
            imaginary=self.__get_values(steps, "imaginary"),
            amplitude=self.__get_values(steps, "amplitude"),
            phase=self.__get_values(steps, "phase"),
            excitationAmplitude=self.__get_values(steps, "excitationAmplitude"),
            soc=steps[0].socStart,
            capacity=steps[0].capacity,
            temperature=np.average(
                [s.temperatureMean for s in steps],
                weights=[s.duration or 1 for s in steps],
            ),
        )

    def __get_values(self, steps: typing.List[Step], attr):
        return [getattr(s, attr) for s in steps]

import typing
from abc import ABC, abstractmethod

from bdat.entities import BatterySpecies, Cycling
from bdat.entities.patterns.pattern_eval import PatternEval
from bdat.entities.steps.step import CyclingStep, EISStep, Step
from bdat.entities.test.cycling_data import CyclingData
from bdat.entities.test.eis_data import EISData
from bdat.steps.steplist_pattern import Match, SteplistPattern


class BaseEvalPattern(ABC):
    @abstractmethod
    def pattern(self, species: BatterySpecies) -> SteplistPattern:
        pass

    def eval_needs_data(self) -> bool:
        return False


class EvalPattern(BaseEvalPattern):

    @abstractmethod
    def eval(
        self,
        test: Cycling,
        match: Match,
        steps: typing.List[Step],
        df: CyclingData | None,
    ) -> PatternEval:
        pass


class EISEvalPattern(BaseEvalPattern):
    @abstractmethod
    def eval(
        self,
        test: Cycling,
        match: Match,
        steps: typing.List[Step],
        df: EISData | None,
    ) -> PatternEval:
        pass

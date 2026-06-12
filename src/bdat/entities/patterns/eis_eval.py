import typing
from dataclasses import dataclass, field

from bdat.entities.patterns.pattern_eval import PatternEval


@dataclass
class EISEval(PatternEval):
    batteryVoltage: typing.List[float]
    frequency: typing.List[float]
    real: typing.List[float]
    imaginary: typing.List[float]
    amplitude: typing.List[float]
    phase: typing.List[float]
    excitationAmplitude: typing.List[float]
    soc: float | None
    capacity: float | None
    temperature: float | None

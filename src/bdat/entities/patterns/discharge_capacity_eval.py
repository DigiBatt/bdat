from dataclasses import dataclass, field

from bson import ObjectId

from bdat.entities.patterns.pattern_eval import PatternEval


@dataclass
class DischargeCapacityEval(PatternEval):
    chargeCurrent: float
    eocVoltage: float
    cvDuration: float | None
    pauseDuration: float
    relaxedVoltage: float
    dischargeCurrent: float
    dischargeDuration: float
    capacity: float
    eodVoltage: float
    cutoffCurrent: float | None = None
    ccDuration: float | None = None

from dataclasses import dataclass, field

from bson import ObjectId

from bdat.entities.patterns.pattern_eval import PatternEval


@dataclass
class FullChargeEval(PatternEval):
    chargeCurrent: float | None
    eocVoltage: float | None
    cvDuration: float | None
    cutoffCurrent: float | None = None
    ccDuration: float | None = None

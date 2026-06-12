from dataclasses import dataclass, field

import numpy as np

from bdat.database.storage.entity import Embedded, Entity


@dataclass
class Step(Embedded):
    stepId: int  #: index of this steps within the test
    start: float  #: start of this step, counted in seconds from the start of the test
    end: float  #: end of this step, counted in seconds from the start of the test
    rowStart: int  #: first row in the test data that belongs to this step, inclusive
    rowEnd: int  #: last row in the test data that belongs to this step, exclusive
    duration: float  #: duration of this step in seconds
    charge: float  #: charge transferred during this step in Ah, charge is positive, discharge is negative
    startTime: float | None  #: start time of the step as unix timestamp in seconds
    endTime: float | None  #: end time of the step as unix timestamp in seconds

    temperatureStart: float | None = None  #: temperature at the start of the step in °C
    temperatureEnd: float | None = None  #: temperature at the end of the step in °C
    temperatureMin: float | None = None  #: minimum temperature during the step in °C
    temperatureMax: float | None = None  #: maximum temperature during the step in °C
    temperatureMean: float | None = None  #: mean temperature during the step in °C

    socStart: float | None = field(
        init=False, default=None
    )  #: SOC at the start of the step in percent
    socEnd: float | None = field(
        init=False, default=None
    )  #: SOC at the start of the step in percent
    chargeStart: float | None = field(
        init=False, default=None
    )  #: total charged capacity of the battery at the start of this step in Ah
    chargeEnd: float | None = field(
        init=False, default=None
    )  #: total charged capacity of the battery at the end of this step in Ah
    dischargeStart: float | None = field(
        init=False, default=None
    )  #: total discharged capacity of the battery at the start of this step in Ah
    dischargeEnd: float | None = field(
        init=False, default=None
    )  #: total discharged capacity of the battery at the end of this step in Ah
    ageStart: float | None = field(
        init=False, default=None
    )  #: total age of the battery at the start of this step counted from the start of the first known test in seconds
    ageEnd: float | None = field(
        init=False, default=None
    )  #: total age of the battery at the end of this step counted from the start of the first known test in seconds
    capacity: float | None = field(
        init=False, default=None
    )  #: capacity of the battery measured in the last capacity test before this step in Ah

    def asCC(self) -> "CCStep":
        """Returns this step as a *CCStep*. Raises a *RuntimeError* if the step is of another steptype."""
        if isinstance(self, CCStep):
            return self
        raise RuntimeError("Not a CC step")

    def asCV(self) -> "CVStep":
        """Returns this step as a *CVStep*. Raises a *RuntimeError* if the step is of another steptype."""
        if isinstance(self, CVStep):
            return self
        raise RuntimeError("Not a CV step")

    def asCP(self) -> "CPStep":
        """Returns this step as a *CPStep*. Raises a *RuntimeError* if the step is of another steptype."""
        if isinstance(self, CPStep):
            return self
        raise RuntimeError("Not a CP step")

    def asPause(self) -> "Pause":
        """Returns this step as a *Pause*. Raises a *RuntimeError* if the step is of another steptype."""
        if isinstance(self, Pause):
            return self
        raise RuntimeError("Not a pause step")

    def asEIS(self) -> "EISStep":
        """Returns this step as a *EISStep*. Raises a *RuntimeError* if the step is of another steptype."""
        if isinstance(self, EISStep):
            return self
        raise RuntimeError("Not a EIS step")

    def getStartVoltage(self) -> float:
        """Returns the voltage at the start of this step in V."""
        if isinstance(self, (CCStep, CPStep, Pause)):
            return self.voltageStart
        elif isinstance(self, CVStep):
            return self.voltage
        raise NotImplementedError()

    def getEndVoltage(self) -> float:
        """Returns the voltage at the end of this step in V."""
        if isinstance(self, (CCStep, CPStep, Pause)):
            return self.voltageEnd
        elif isinstance(self, CVStep):
            return self.voltage
        raise NotImplementedError()

    def getStartCurrent(self) -> float:
        """Returns the current at the start of this step in A."""
        if isinstance(self, CCStep):
            return self.current
        elif isinstance(self, (CVStep, CPStep)):
            return self.currentStart
        elif isinstance(self, Pause):
            return 0
        raise NotImplementedError()

    def getEndCurrent(self) -> float:
        """Returns the current at the end of this step in A."""
        if isinstance(self, CCStep):
            return self.current
        elif isinstance(self, (CVStep, CPStep)):
            return self.currentEnd
        elif isinstance(self, Pause):
            return 0
        raise NotImplementedError()


@dataclass
class CyclingStep(Step):
    maxError: float | None = None
    rmse: float | None = None


@dataclass
class CCStep(CyclingStep):
    current: float = np.nan
    voltageStart: float = np.nan
    voltageEnd: float = np.nan


@dataclass
class CVStep(CyclingStep):
    voltage: float = np.nan
    currentStart: float = np.nan
    currentEnd: float = np.nan


@dataclass
class CPStep(CyclingStep):
    power: float = np.nan
    voltageStart: float = np.nan
    voltageEnd: float = np.nan
    currentStart: float = np.nan
    currentEnd: float = np.nan


@dataclass
class Pause(CyclingStep):
    voltageStart: float = np.nan
    voltageEnd: float = np.nan


@dataclass
class EISStep(Step):
    batteryVoltage: float | None = None
    frequency: float | None = None
    real: float | None = None
    imaginary: float | None = None
    amplitude: float | None = None
    phase: float | None = None
    excitationAmplitude: float | None = None

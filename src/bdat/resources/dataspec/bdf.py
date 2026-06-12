import typing

import pandas as pd

from bdat.entities.dataspec.charge_spec import (
    Calculate,
    ChargeSpec,
    FourColumns,
    SeparateColumns,
)
from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec, Unit
from bdat.entities.dataspec.data_spec import CyclingDataSpec
from bdat.entities.dataspec.time_format import Seconds, Timestamp


class BDFDataSpec(CyclingDataSpec):
    def __init__(
        self,
        timeUnit: Unit = Unit.BASE,
        currentUnit: Unit = Unit.BASE,
        timestamp: bool = True,
        chargeCapacity: bool = True,
        dischargeCapacity: bool = True,
        stepCapacity: bool = True,
        netCapacity: bool = True,
        temperature: bool = True,
        power: bool = True,
        stepNumber: bool = True,
        cycleNumber: bool = True,
        ambientTemperature: bool = True,
        procedureLevel: bool = False,
    ):
        duration = TimeColumnSpec("Test Time / s", Seconds(unit=timeUnit))
        timeColumn = None
        if timestamp:
            timeColumn = TimeColumnSpec("Unix Time / s", Timestamp())
        current = ColumnSpec("Current / A", currentUnit)
        if chargeCapacity and dischargeCapacity:
            chargeColumn = ColumnSpec("Charging Capacity / Ah")
            dischargeColumn = ColumnSpec("Discharging Capacity / Ah")
            if stepCapacity and netCapacity:
                stepChargeColumn = ColumnSpec("Step Capacity / Ah")
                netChargeColumn = ColumnSpec("Net Capacity / Ah")
                chargeSpec: ChargeSpec = FourColumns(
                    chargeColumn, dischargeColumn, netChargeColumn, stepChargeColumn
                )
            else:
                chargeSpec = SeparateColumns(chargeColumn, dischargeColumn)
        else:
            chargeSpec = Calculate(current, duration)
        super().__init__(
            "bdf",
            duration,
            timeColumn,
            current,
            ColumnSpec("Voltage / V"),
            chargeSpec,
            ColumnSpec("Surface Temperature T1 / degC") if temperature else None,
            ColumnSpec("Power / W") if power else None,
            ColumnSpec("Step Count / 1") if stepNumber else None,
            ColumnSpec("Cycle Count / 1") if cycleNumber else None,
            ColumnSpec("Ambient Temperature / degC") if ambientTemperature else None,
            ColumnSpec("Procedure Level / 1") if procedureLevel else None,
        )

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> "BDFDataSpec":
        timestamp = "Unix Time / s" in df.columns
        chargeCapacity = "Charging Capacity / Ah" in df.columns
        dischargeCapacity = "Discharging Capacity / Ah" in df.columns
        stepCapacity = "Step Capacity / Ah" in df.columns
        netCapacity = "Net Capacity / Ah" in df.columns
        temperature = "Surface Temperature T1 / degC" in df.columns
        power = "Power / W" in df.columns
        stepNumber = "Step Count / 1" in df.columns
        cycleNumber = "Cycle Count / 1" in df.columns
        ambientTemperature = "Ambient Temperature / degC" in df.columns
        procedureLevel = "Procedure Level / 1" in df.columns
        return BDFDataSpec(
            timestamp=timestamp,
            chargeCapacity=chargeCapacity,
            dischargeCapacity=dischargeCapacity,
            stepCapacity=stepCapacity,
            netCapacity=netCapacity,
            temperature=temperature,
            power=power,
            stepNumber=stepNumber,
            cycleNumber=cycleNumber,
            ambientTemperature=ambientTemperature,
            procedureLevel=procedureLevel,
        )

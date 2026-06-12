import typing

import pandas as pd

from bdat.entities.dataspec.charge_spec import Calculate, SeparateColumns
from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec, Unit
from bdat.entities.dataspec.data_spec import CyclingDataSpec
from bdat.entities.dataspec.time_format import Seconds


class BMConvertedDataSpec(CyclingDataSpec):
    def __init__(
        self,
        timeName: str,
        timeUnit: Unit = Unit.BASE,
        currentUnit: Unit = Unit.BASE,
        chargeName: str = "AhCha#Ah",
        temperatureName: str | None = None,
    ):
        if temperatureName:
            temperatureColumn = ColumnSpec(temperatureName, Unit.BASE)
        else:
            temperatureColumn = None
        super().__init__(
            "bm",
            TimeColumnSpec(timeName, Seconds(unit=timeUnit)),
            None,
            ColumnSpec("Current#A", currentUnit),
            ColumnSpec("Voltage#V"),
            SeparateColumns(
                chargeColumn=ColumnSpec(chargeName),
                dischargeColumn=ColumnSpec("AhDch#Ah"),
            ),
            temperatureColumn,
        )

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> "BMConvertedDataSpec":
        temperatureName = "T1#degC" if "T1#degC" in df.columns else None
        if "Program Duration#s" in df.columns:
            timeUnit = Unit.BASE
            timeName = "Program Duration#s"
        else:
            timeUnit = Unit.MILLI
            timeName = "Program Duration#ms"
        if "AhCha#AH" in df.columns:
            chargeName = "AhCha#AH"
        else:
            chargeName = "AhCha#Ah"
        return BMConvertedDataSpec(
            timeName=timeName,
            timeUnit=timeUnit,
            chargeName=chargeName,
            temperatureName=temperatureName,
        )

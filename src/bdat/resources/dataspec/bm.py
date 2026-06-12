import typing

import pandas as pd

from bdat.entities.dataspec.charge_spec import ChargeSpec, FourColumns, SeparateColumns
from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec, Unit
from bdat.entities.dataspec.data_spec import CyclingDataSpec
from bdat.entities.dataspec.time_format import Seconds, Timestamp


class BMDataSpec(CyclingDataSpec):
    def __init__(
        self,
        timeUnit: Unit = Unit.MILLI,
        timeName: str | None = None,
        currentUnit: Unit = Unit.BASE,
        chargeName: str = "AhLad#AhCha#D",
        dischargeName: str = "AhEla#AhDch#D",
        diffChargeName: str | None = "AhAkku#Ah#D",
        stepChargeName: str | None = "AhStep#AhStep#D",
        temperatureName: str | None = None,
        ambientTemperatureName: str | None = None,
    ):
        timeColumn = None
        if timeName:
            timeColumn = TimeColumnSpec(timeName, Timestamp())
        temperatureColumn = None
        ambientTemperatureColumn = None
        if temperatureName:
            temperatureColumn = ColumnSpec(temperatureName, Unit.BASE)
        if ambientTemperatureName:
            ambientTemperatureColumn = ColumnSpec(ambientTemperatureName, Unit.BASE)
        chargeColumn = ColumnSpec(chargeName)
        dischargeColumn = ColumnSpec(dischargeName)
        if diffChargeName and stepChargeName:
            chargeSpec: ChargeSpec = FourColumns(
                chargeColumn,
                dischargeColumn,
                ColumnSpec(diffChargeName),
                ColumnSpec(stepChargeName),
            )
        else:
            chargeSpec = SeparateColumns(chargeColumn, dischargeColumn)
        super().__init__(
            "bm",
            TimeColumnSpec("Programmdauer##D", Seconds(unit=timeUnit)),
            timeColumn,
            ColumnSpec("Strom#A#D", currentUnit),
            ColumnSpec("Spannung#V#D"),
            chargeSpec,
            temperatureColumn,
            None,
            ColumnSpec("Schritt##I"),
            ColumnSpec("Zyklus##I"),
            ambientTemperatureColumn,
            ColumnSpec("Prozedurebene##I"),
        )

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> "BMDataSpec":
        temperatureName = "T1#C1#D" if "T1#C1#D" in df.columns else None
        ambientTemperatureName = "Tenv#Cenv#D" if "Tenv#Cenv#D" in df.columns else None
        if "AhLad#AhCha#D" in df.columns:
            chargeName = "AhLad#AhCha#D"
        else:
            chargeName = "AhLad#AhLad#D"
        if "AhEla#AhDch#D" in df.columns:
            dischargeName = "AhEla#AhDch#D"
        else:
            dischargeName = "AhEla#AhEla#D"
        timeName = None
        for col in df.columns:
            if col.startswith("Zeit##T"):
                timeName = col
        return BMDataSpec(
            timeName=timeName,
            chargeName=chargeName,
            dischargeName=dischargeName,
            temperatureName=temperatureName,
            ambientTemperatureName=ambientTemperatureName,
        )

import pandas as pd

from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec, Unit
from bdat.entities.dataspec.data_spec import EISDataSpec
from bdat.entities.dataspec.time_format import Seconds, Timestamp


class InspectrumDataSpec(EISDataSpec):
    def __init__(
        self,
        df: pd.DataFrame,
        timeUnit: Unit = Unit.BASE,
    ):
        timeColumn = None
        temperatureColumn = None
        for col in df.columns:
            if col.startswith("Zeit##T"):
                timeColumn = TimeColumnSpec(col, Timestamp())
            elif col.startswith("LogTemp"):
                temperatureColumn = ColumnSpec(col)

        super().__init__(
            id="eismeter",
            durationColumn=TimeColumnSpec("Programmdauer##D", Seconds(unit=timeUnit)),
            timeColumn=timeColumn,
            batteryVoltageColumn=ColumnSpec("Spannung#V#D"),
            frequencyColumn=ColumnSpec("Freq#InspHz#D"),
            realColumn=ColumnSpec("Re#InspOhm#D"),
            imaginaryColumn=ColumnSpec("Im#InspOhm#D"),
            amplitudeColumn=ColumnSpec("Amp#InspOhm#D"),
            phaseColumn=ColumnSpec("Phase#InspRad#D"),
            excitationAmplitudeColumn=ColumnSpec("ExcAmp#InspA#D"),
            temperatureColumn=temperatureColumn,
        )

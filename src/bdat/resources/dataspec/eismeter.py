import pandas as pd

from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec, Unit
from bdat.entities.dataspec.data_spec import EISDataSpec
from bdat.entities.dataspec.time_format import Seconds, Timestamp


class EISMeterDataSpec(EISDataSpec):
    def __init__(
        self,
        df: pd.DataFrame,
        timeUnit: Unit = Unit.BASE,
    ):
        timeColumn = None
        for col in df.columns:
            if col.startswith("Zeit##T"):
                timeColumn = TimeColumnSpec(col, Timestamp())
        super().__init__(
            id="eismeter",
            durationColumn=TimeColumnSpec("Programmdauer##D", Seconds(unit=timeUnit)),
            timeColumn=timeColumn,
            batteryVoltageColumn=ColumnSpec("U1#EIS#D"),
            frequencyColumn=ColumnSpec("ActFreq#EIS#D"),
            realColumn=ColumnSpec("Zreal1#EIS#D"),
            imaginaryColumn=ColumnSpec("Zimg1#EIS#D"),
            amplitudeColumn=ColumnSpec("Betrag#EIS#D"),
            phaseColumn=ColumnSpec("Phase#EIS#D"),
            excitationAmplitudeColumn=ColumnSpec("AAmplitude#EIS#D"),
        )

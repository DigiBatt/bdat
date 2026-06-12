from bdat.entities.dataspec.charge_spec import Calculate
from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec, Unit
from bdat.entities.dataspec.data_spec import CyclingDataSpec
from bdat.entities.dataspec.time_format import Seconds, Timestamp

DefaultTargetSpec = CyclingDataSpec(
    "normalized",
    TimeColumnSpec("Duration", Seconds()),
    TimeColumnSpec("Time", Timestamp()),
    ColumnSpec("Current", Unit.BASE),
    ColumnSpec("Voltage", Unit.BASE),
    Calculate(ColumnSpec("Current", Unit.BASE), TimeColumnSpec("Duration", Seconds())),
)

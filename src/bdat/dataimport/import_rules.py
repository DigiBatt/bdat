import bdat.entities as entities
from bdat.entities.dataspec.charge_spec import SeparateColumns
from bdat.entities.dataspec.column_spec import ColumnSpec
from bdat.entities.dataspec.data_spec import DataSpec
from bdat.entities.dataspec.unit import Unit
from bdat.exceptions import NoCyclingDataException
from bdat.resources.dataspec.bm import BMDataSpec
from bdat.resources.dataspec.neware import NewareAhjoDataSpec, NewareCorvusDataSpec


def could_be_cycling(test: entities.Cycling) -> bool:
    if test.title.endswith("NoName_VA") or test.title.endswith("NoName_MSG"):
        return False
    if test.title.startswith("aux_data_"):
        return False
    if test.tool is not None and test.tool.title.startswith("Kreis"):
        if test.parent is None:
            return False
    if test.tool is not None and test.tool.title.lower().startswith("eis"):
        return False
    return True


# TODO: temporary solution, this should actually look at the data and the resulting dataspec should be pushed to the database
# TODO: this could directly return a CyclingData instance


def get_dataspec(test: entities.Cycling, df) -> DataSpec:
    if test.title.endswith("NoName_VA") or test.title.endswith("NoName_MSG"):
        raise NoCyclingDataException(test)
    try:
        spec: DataSpec = NewareAhjoDataSpec(test, df)
        return spec
    except:
        pass
    try:
        spec = NewareCorvusDataSpec(test, df)
        if spec.tryOnTest(df):
            df["Temperature [degC]"] = 25
            spec.temperatureColumn = ColumnSpec("Temperature [degC]")
            return spec
    except:
        pass
    try:
        if "T1#C1#D" in df.columns:
            spec = BMDataSpec(timeUnit=Unit.MILLI, temperatureName="T1#C1#D")
            if spec.tryOnTest(df):
                return spec
        else:
            spec = BMDataSpec(timeUnit=Unit.MILLI)
            if spec.tryOnTest(df):
                return spec
    except:
        pass

    raise RuntimeError(
        f"Could not find suitable dataspec for test (columns: {df.columns})"
    )

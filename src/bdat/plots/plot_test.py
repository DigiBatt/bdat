import typing

import pandas as pd

import bdat.entities as entities
from bdat.database.storage.entity import Entity
from bdat.database.storage.storage import Storage
from bdat.dataimport import import_rules
from bdat.entities.dataspec.column_spec import Unit
from bdat.entities.plots import Plotdata
from bdat.plots.plot import plot


@plot("test")
def plot_test(storage: Storage, test: Entity) -> Plotdata:
    if not isinstance(test, entities.Cycling):
        raise Exception("Invalid resource type")
    if not test:
        raise Exception("Could not find resource")
    datafile = storage.get_file(test.res_id_or_raise())
    if datafile is None:
        raise Exception("Test has no data")
    df = pd.read_parquet(datafile)
    dataspec = import_rules.get_dataspec(test, df)
    duration = dataspec.durationColumn.timeFormat.toSeconds(
        df[dataspec.durationColumn.name].to_numpy()
    )
    timeBins = pd.cut(duration, 1000, labels=False)
    columns = [
        (dataspec.currentColumn, "current"),
        (dataspec.voltageColumn, "voltage"),
    ]
    if dataspec.temperatureColumn:
        columns.append((dataspec.temperatureColumn, "temperature"))
    dfValues = df[[spec.name for spec, _ in columns]].copy()
    dfValues["time"] = duration
    dfValues = dfValues.groupby(timeBins).mean()
    for spec, _ in columns:
        dfValues[spec.name] = spec.unit.convert(
            dfValues[spec.name].to_numpy(), Unit.BASE
        )
    dfValues.rename(
        columns={spec.name: title for spec, title in columns},
        inplace=True,
    )
    return Plotdata(
        "test plot", test, "test", {"data": dfValues.to_dict(orient="records")}
    )
